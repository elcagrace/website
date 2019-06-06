import os

import re

from collections import defaultdict

from datetime import date
from dateutil.relativedelta import relativedelta

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from markdown.util import etree

from .parameters import parameters
from .calendar import get_events_by_horizon, format_calendar

# Constants and Utility

NONANCHOR_CHARACTERS = re.compile(r'\W+')


def make_anchor(string):
    return NONANCHOR_CHARACTERS.sub('-', string.lower()) if string is not None else '-'


EXPLICIT_ANCHOR = re.compile(r'\{anchor:([\w-]+)\}\n((?:.|\n)*)', re.MULTILINE)


def get_paragraph_anchor_and_text(paragraph):
    if paragraph.text is not None:
        match = EXPLICIT_ANCHOR.fullmatch(paragraph.text)
        if match is not None:
            return match.group(1), match.group(2)
    return None, paragraph.text


FORM_OPEN = re.compile(r'\{begin_form\}', re.MULTILINE)
FORM_CLOSE = re.compile(r'\{end_form\}', re.MULTILINE)


def is_form_open(paragraph):
    return paragraph.text is not None and bool(FORM_OPEN.fullmatch(paragraph.text))


def is_form_close(paragraph):
    return paragraph.text is not None and bool(FORM_CLOSE.fullmatch(paragraph.text))


SNIPPET_INCLUSION = re.compile(r'\{include:([\w-]+)\}', re.MULTILINE)


def get_snippet(paragraph):
    if paragraph.text is not None:
        match = SNIPPET_INCLUSION.fullmatch(paragraph.text)
        if match is not None:
            with open(f'content/snippets/{match.group(1)}.html', encoding='utf-8') as source_file:
                return source_file.read()
    return None


SNIPPET_SUBSTITUTION = re.compile(r'\{substitute:([\w-]+)\}', re.MULTILINE)


def get_substitution(paragraph, substitutions):
    if paragraph.text is not None:
        match = SNIPPET_SUBSTITUTION.fullmatch(paragraph.text)
        if match is not None:
            with_defaults = defaultdict(lambda: '')
            with_defaults.update(substitutions)
            with open(f'content/snippets/{match.group(1)}.html', encoding='utf-8') as source_file:
                return source_file.read().format_map(with_defaults)
    return None


GREETERS_INCLUSION = re.compile(r'\{greeters\}', re.MULTILINE)


def get_greeters(paragraph):
    if paragraph.text is not None and GREETERS_INCLUSION.fullmatch(paragraph.text):
        results = []
        today = date.today()
        i = date(today.year, today.month, 1) + relativedelta(months=1)
        for _ in range(7):
            path = i.strftime('content/greeters/%Y-%B.pdf')
            previous = i - relativedelta(months=1)
            if os.path.isfile(path):
                results.append((f'The {i.strftime("%B")} Greeter (published in {previous.strftime("%B")}) (PDF)', path))
            i = previous
        return results
    return None


CAROUSEL_INCLUSION = re.compile(r'\{carousel\}', re.MULTILINE)
CAROUSEL_DIRECTORY = 'content/images/carousel'


def get_carousel(paragraph):
    if paragraph.text is not None and CAROUSEL_INCLUSION.fullmatch(paragraph.text):
        results = []
        for filename in os.listdir(CAROUSEL_DIRECTORY):
            if filename.endswith('.jpeg'):
                results.append(os.path.join(CAROUSEL_DIRECTORY, filename))
        return results
    return None


UPCOMING_EVENTS_INCLUSION = re.compile(r'\{upcoming_events\}', re.MULTILINE)
FEATURED_EVENT_PATTERN = re.compile(r'(.*[^\s])\s*\(featured\)\s*', re.IGNORECASE)


def cleanup_event_name(name):
    result = FEATURED_EVENT_PATTERN.sub(
        lambda match: match.group(1),
        name,
    )
    if result.endswith('*'):
        return result[:-1]
    return result


def stable_group_by(sequence, key):
    results = []
    indices = {}
    for item in sequence:
        signature = key(item)
        index = indices.get(signature)
        if index is None:
            indices[signature] = len(results)
            results.append([item])
        else:
            results[index].append(item)
    return results


def to_date(event):
    return date.fromordinal(event.start.toordinal())


def to_runs(events):
    seed = to_date(events[0])
    endpoints = [[seed, seed]]
    for event in events:
        prior = endpoints[-1][1]
        expected = prior + relativedelta(days=1)
        current = to_date(event)
        if current in (prior, expected):
            endpoints[-1][1] = current
        else:
            endpoints.append([current, current])
    runs = []
    for start, end in endpoints:
        prefix = start.strftime('%B&nbsp;%-d')
        if start == end:
            runs.append(prefix)
        elif start.month == end.month:
            runs.append(f'{prefix}–end.strftime("%d-")')
        else:
            runs.append(f'{prefix}–end.strftime("%B&nbsp;%-d")')
    if len(runs) == 1:
        return runs[0]
    if len(runs) == 2:
        return f'{runs[0]} and {runs[1]}'
    return f'{", ".join(runs[:-1])}, and {runs[-1]}'


def get_upcoming_events(paragraph):
    if paragraph.text is not None and UPCOMING_EVENTS_INCLUSION.fullmatch(paragraph.text):
        events = get_events_by_horizon(31, FEATURED_EVENT_PATTERN)
        grouped_events = stable_group_by(events, lambda event: (event.name, event.location, event.notes))
        results = []
        for group in grouped_events:
            event = group[0]
            name = f'{cleanup_event_name(event.name)}<br>{to_runs(group)}'
            url = f'resources.cgi?year={event.start.year}&month={event.start.month}#{event.anchor}'
            results.append((name, url))
        return results
    return None


CALENDAR_INCLUSION = re.compile(r'\{calendar\}', re.MULTILINE)


def is_calendar(paragraph):
    return paragraph.text is not None and bool(CALENDAR_INCLUSION.fullmatch(paragraph.text))


HALF_WIDTH = re.compile(r'(.*) \(1/2\)')
THIRD_WIDTH = re.compile(r'(.*) \(1/3\)')


HALF_WIDTH_CLASS = '6u 12u(2) 12u(3)'
THIRD_WIDTH_CLASS = '4u 12u(2) 12u(3)'


TOTAL_WIDTH = 6


WIDTHS = {
    HALF_WIDTH_CLASS: 3,
    THIRD_WIDTH_CLASS: 2,
}


def get_heading_text_and_section_class(heading):
    text, element_class = heading.text, None
    if text is not None:
        match = HALF_WIDTH.fullmatch(heading.text)
        if match is not None:
            text, element_class = match.group(1), HALF_WIDTH_CLASS
        match = THIRD_WIDTH.fullmatch(heading.text)
        if match is not None:
            text, element_class = match.group(1), THIRD_WIDTH_CLASS
    return text, element_class


# Base Classes

class ElementTransformer(Treeprocessor):
    def transform(self, element):
        raise NotImplementedError

    def run(self, element):
        self.transform(element)
        for child in element:
            self.run(child)


# Skip Transformers

class CollectHeadingLinks(Treeprocessor):
    @staticmethod
    def collect_links(element):
        if element.tag == 'h1':
            text, _ = get_heading_text_and_section_class(element)
            yield make_anchor(text), text
        for child in element:
            yield from CollectHeadingLinks.collect_links(child)

    def run(self, element):
        root = etree.Element('div')
        links = tuple(CollectHeadingLinks.collect_links(element))
        if len(links) > 1:
            navigation = etree.Element(
                'nav',
                attrib={
                    'id': 'skip',
                },
            )
            navigation.text = 'Skip to '
            for anchor, text in links:
                link = etree.Element(
                    'a',
                    attrib={
                        'href': f'#{anchor}',
                    },
                )
                link.text = text
                link.tail = ' '
                navigation.append(link)
            navigation[-1].tail = ''
            cell = etree.Element(
                'div',
                attrib={
                    'class': '12u',
                },
            )
            cell.append(navigation)
            row = etree.Element(
                'div',
                attrib={
                    'class': 'row',
                },
            )
            row.append(cell)
            root.append(row)
        return root


# Content Transformers

class CreateAnchors(ElementTransformer):
    def transform(self, element):
        if element.tag == 'p':
            anchor, element.text = get_paragraph_anchor_and_text(element)
            if anchor is not None:
                element.set('id', anchor)


class ExternalizeLinks(ElementTransformer):
    def transform(self, element):
        if element.tag == 'a':
            href = element.get('href')
            if href is not None and href.startswith('http'):
                element.set('target', '_blank')


class IncludeFormTags(ElementTransformer):
    def transform(self, element):
        accumulator = []
        inside_form = False
        for i, child in enumerate(element):
            if child.tag == 'p' and is_form_open(child):
                child.tag = 'form'
                child.text = ''
                child.set('method', 'post')
                accumulator.append(child)
                inside_form = True
            elif inside_form:
                if child.tag == 'p' and is_form_close(child):
                    inside_form = False
                else:
                    accumulator[-1].append(child)
            else:
                accumulator.append(child)
        element[:] = accumulator


class IncludeSnippets(ElementTransformer):
    def transform(self, element):
        if element.tag == 'p':
            snippet = get_snippet(element)
            if snippet is not None:
                element.tag = 'div'
                element.text = self.md.htmlStash.store(snippet)


class IncludeSubstitutions(ElementTransformer):
    def __init__(self, substitutions):
        super().__init__()
        self.substitutions = substitutions

    def transform(self, element):
        if element.tag == 'p':
            substitution = get_substitution(element, self.substitutions)
            if substitution is not None:
                element.tag = 'div'
                element.text = self.md.htmlStash.store(substitution)


class IncludeCarousel(ElementTransformer):
    def transform(self, element):
        if element.tag == 'p':
            carousel = get_carousel(element)
            if carousel is not None:
                element.tag = 'div'
                element.text = ''
                element.set('class', 'inline')
                element.set('id', 'index-carousel')
                element.set('style', 'max-width: 400px;')
                for i, url in enumerate(carousel):
                    image = etree.Element(
                        'img',
                        attrib={
                            'alt': '',
                            'class': 'inline',
                            'src': url,
                        },
                    )
                    if i > 0:
                        image.set('style', 'display: none;')
                    element.append(image)


class IncludeUpcomingEvents(ElementTransformer):
    def transform(self, element):
        if element.tag == 'p':
            events = get_upcoming_events(element)
            if events is not None:
                element.tag = 'ul'
                element.text = ''
                for name, url in events:
                    link = etree.Element(
                        'a',
                        attrib={
                            'href': url,
                        },
                    )
                    link.text = self.md.htmlStash.store(name)
                    item = etree.Element('li')
                    item.append(link)
                    element.append(item)


class IncludeCalendar(ElementTransformer):
    def transform(self, element):
        if element.tag == 'p' and is_calendar(element):
            try:
                year = int(parameters.getfirst('year'))
            except:
                year = None
            try:
                month = int(parameters.getfirst('month'))
            except:
                month = None
            element.tag = 'div'
            element.text = self.md.htmlStash.store(format_calendar(year, month, cleanup=cleanup_event_name))


class IncludeGreeters(ElementTransformer):
    def transform(self, element):
        if element.tag == 'p':
            greeters = get_greeters(element)
            if greeters is not None:
                element.tag = 'ul'
                element.text = ''
                for name, url in greeters:
                    link = etree.Element(
                        'a',
                        attrib={
                            'href': url,
                        },
                    )
                    link.text = name
                    item = etree.Element('li')
                    item.append(link)
                    element.append(item)


class SectionByHeading(ElementTransformer):
    def __init__(self, heading_tag, build_headingless_sections):
        super().__init__()
        self.heading_tag = heading_tag
        self.build_headingless_sections = build_headingless_sections

    def transform(self, element):
        if element.tag == 'section' and len(element) > 0 and element[0].tag == self.heading_tag:
            return
        accumulator = []
        in_sections = False
        for child in element:
            if child.tag == self.heading_tag:
                if accumulator and not in_sections and self.build_headingless_sections:
                    headingless_section = etree.Element('section')
                    headingless_section[:] = accumulator
                    accumulator = [headingless_section]
                child.text, element_class = get_heading_text_and_section_class(child)
                accumulator.append(etree.Element(
                    'section',
                    attrib={
                        'id': make_anchor(child.text),
                    },
                ))
                if element_class is not None:
                    accumulator[-1].set('class', element_class)
                in_sections = True
            if in_sections:
                accumulator[-1].append(child)
            else:
                accumulator.append(child)
        element[:] = accumulator


class SectionByH1(SectionByHeading):
    def __init__(self):
        super().__init__('h1', True)


class SectionByH2(SectionByHeading):
    def __init__(self):
        super().__init__('h2', False)


class OrganizeIntoRows(ElementTransformer):
    @staticmethod
    def create_row(already_within_section):
        division = etree.Element(
            'div',
            attrib={
                'class': 'row',
            },
        )
        if already_within_section:
            return division
        section = etree.Element('section')
        section.append(division)
        return section

    def transform(self, element):
        if element.get('class') == 'row':
            return
        already_within_section = element.tag == 'section'
        accumulator = []
        fill = None
        for child in element:
            if fill is None:
                if child.tag == 'section' and child.get('class') in WIDTHS:
                    accumulator.append(OrganizeIntoRows.create_row(already_within_section))
                    fill = 0
                else:
                    accumulator.append(child)
            if fill is not None:  # intentionally not an elif (see `fill = 0` above)
                width = WIDTHS.get(child.get('class'))
                if width is None:
                    accumulator.append(child)
                    fill = None
                else:
                    if fill + width > TOTAL_WIDTH:
                        accumulator.append(OrganizeIntoRows.create_row(already_within_section))
                        fill = 0
                    row = accumulator[-1] if element.tag == 'section' else accumulator[-1][0]
                    row.append(child)
                    fill += width
        element[:] = accumulator


class IncreaseHeadingDepth(ElementTransformer):
    HEADING_DEPTH_INCREASE = {f'h{i}': f'h{i + 1}' for i in range(1, 6)}

    def transform(self, element):
        new_tag = IncreaseHeadingDepth.HEADING_DEPTH_INCREASE.get(element.tag)
        if new_tag is not None:
            element.tag = new_tag


class WrapInContentDiv(Treeprocessor):
    def __init__(self, element_class, element_id):
        super().__init__()
        self.element_class = element_class
        self.element_id = element_id

    def run(self, element):
        division = etree.Element('div')
        if self.element_class is not None:
            division.set('class', self.element_class)
        if self.element_id is not None:
            division.set('id', self.element_id)
        division[:] = element
        element[:] = (division,)


# Sidebar-Specific Transformers

class EventifyLists(ElementTransformer):
    def transform(self, element):
        if element.tag == 'ul':
            element.set('class', 'events')


# Index-Specific Transformers

class UnbulletLists(ElementTransformer):
    def transform(self, element):
        if element.tag == 'ul':
            element.set('class', 'unbulleted')


# Flavors

def register(md, transformer):
    md.treeprocessors.register(transformer, transformer.__class__.__name__, -1)
    transformer.md = md


class SkipFlavor(Extension):
    def extendMarkdown(self, md):
        register(md, CollectHeadingLinks())


class ContentFlavor(Extension):
    def extendMarkdown(self, md):
        register(md, CreateAnchors())
        register(md, ExternalizeLinks())
        register(md, IncludeFormTags())
        register(md, IncludeSnippets())
        register(md, IncludeSubstitutions({}))
        register(md, IncludeCarousel())
        register(md, IncludeUpcomingEvents())
        register(md, IncludeCalendar())
        register(md, IncludeGreeters())
        register(md, SectionByH1())
        register(md, SectionByH2())
        register(md, OrganizeIntoRows())
        register(md, IncreaseHeadingDepth())
        register(md, WrapInContentDiv('12u', 'content'))


class SidebarFlavor(ContentFlavor):
    def extendMarkdown(self, md):
        super().extendMarkdown(md)
        register(md, WrapInContentDiv('3u 12u(2) 12u(3)', 'sidebar'))
        register(md, EventifyLists())


class IndexFlavor(ContentFlavor):
    def extendMarkdown(self, md):
        super().extendMarkdown(md)
        register(md, WrapInContentDiv('9u 12u(2) 12u(3)', 'content'))
        register(md, UnbulletLists())


class FormFlavor(ContentFlavor):
    def __init__(self, substitutions):
        super().__init__()
        self.substitutions = substitutions

    def extendMarkdown(self, md):
        super().extendMarkdown(md)
        register(md, IncludeSubstitutions(self.substitutions))

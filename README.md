# Website

This repository holds the content of the `egrace` website.

# File Structure

An outline of the website files is given below.  If you are managing the website
content, you will normally edit files in the `content` folder.

*   The outermost folder contains CGI scripts that make the website content
    available online as well as miscellaneous files, like the site icons or the
    error messages that display if the site is broken.  It should not normally
    be necessary to change this content.

    *   `content` contains the website's text, images, and files.

        *   `content/pages` contains the text content of the website in Markdown
            format.  See below for information on Markdown.

        *   `content/images` contains images used on the site.  Photos should be
            in JPEG format and named `[filename].jpeg` and other images should
            be in PNG or GIF format (with PNG preferred) and named
            `[filename].png` or `[filename].gif`.

            *   `content/images/carousel/` contains the images to display on the
                front-page carousel.  These should be JPEGs that are 400 pixels
                wide and 266 pixels tall.  There can be any number of images in
                this folder as long as there is at least one.

            *   `content/images/logos/` contains other organizations' logos.

        *   `content/greeters` contains the monthly greeters.  These should be
            named in the format `[year]-[month].pdf` so that the website can
            find them and link to them automatically.  For example, the greeter
            for December of 2030 would be named `2030-December.pdf`.

        *   `content/documents` contains other documents that a user might
            download.

        *   `content/snippets` contains other website content in HTML format.
            It should not normally be necessary to change this content.

    *   `theme` contains the website theme, both for desktop and mobile devices.
        It should not normally be necessary to change this content.

        *   `theme/templates` contains the non-content HTML used on the site.

        *   `theme/css` contains the CSS (style rules) used on the site as well
            as any images that are used by those style rules.

        *   `theme/js` contains the client-side code for the site.

        *   `theme/fonts` contains the fonts used on the site.

        *   `theme/icons` contains the icons used on the site.

    *   `server` contains the server-side code for the site.  It should not
        normally be necessary to change this content.

# Markdown

Markdown is a way to style text on the web; almost all of the text on the
website is written as Markdown.  See ["Mastering Markdown" on
GitHub](https://guides.github.com/features/mastering-markdown/) for a quick
introduction.

## Markdown Basics

### Spacing in Markdown

For good style, different parts of the page should be separated by blank lines,
as below:

```
# This is an example heading.

This is an example paragraph.

*   This
*   is
*   an
*   example
*   list.
```

Furthermore, Markdown files should normally end with a single blank line.

Also be careful not to leave spaces or tabs at the end of a line; these extra
spaces can cause formatting problems on the website that might not be obvious at
first glance.

### Headings

Headings are written by putting hash marks (`#`) in front of the heading, with
one hash mark for a top-level heading, two for a subheading, and three for a
subsubheading.

```
# Heading

## Subheading

### Subsubheading
```

A heading for the website can be marked `(1/2)` or `(1/3)` to make the section
underneath of it half- or one-third-width.

```
# Half-Width Heading (1/2)

# One-Third-Width Heading (1/3)
```

### Paragraphs

Paragraphs are written as text across one or more lines and separated by blank
lines:

```
This first paragraph is all on one line.

This second paragraph is on two lines,
and Markdown will treat the line break between those lines like a space.
```

### Lists

Bulleted lists are written with asterisks (`*`), usually followed by three
spaces so that the list items' text is all indented four columns:

```
*   Item
*   Another item
*   Yet another item
```

If the list items contain sentences or paragraphs, place blank lines between
them:

```
*   This is an item.

*   This is another item.

*   This is yet another item.
```

Numbered lists are written with numbers followed by periods:

```
1.  Item
2.  Another item
3.  Yet another item
```

And the same rule applies to numbered lists containing sentences or paragraphs:

```
1.  This is an item.

2.  This is another item.

3.  This is yet another item.
```

### Bold and Italics

Bold text is written by surrounding it with double asterisks:

```
This **word** is bold.
```

Italic text is written by surrounding it with single asterisks:

```
This *word* is italicized.
```

### Links to Webpages

Links to other sites or pages not on the website are written by putting the link
text in square brackets and the URL in parentheses:

```
[the ELCA website](http://elca.org/)
```

Links to another page on our website are written the same way, but only the
`[page].cgi` part of the URL needs to be written:

```
[visit Grace](visit.cgi)
```

### Links to Sections with Headings

A link to a particular section on one of the site's webpages is written like a
link to that webpage, but an *anchor name* also provided after a hash (`#`).
The anchor name for a section with a heading is that heading's text, but
lowercased and with spaces and punctuation replaced by hyphens.  For example, if
the Children's Choir is described as

```
## Children's Choir (1/3)

For elementary students, this group…
```

in `connect.md`, then a link to that description would be written like

```
[the Children's Choir](connect.cgi#children-s-choir)
```

because the `(1/3)` does not count as part of the heading, and the apostrophe
and space are both replaced with hyphens.

### Links to Calendar Events

A link to a particular calendar event is written like a link to a section with a
heading, but the link should specify the year and month of the event (so that
the appropriate page of the calendar is opened), and the anchor name should be
based off the name of the event rather than a heading.

For instance, a link to a "Children's Choir Practice" event during December 2030
would be written

```
[Children's Choir Practice](resources.cgi?year=2030&month=12#children-s-choir-practice)
```

### Links to Parts of the Interior Map

The URLs for different parts of the building interior map are listed below:

*   `visit.cgi#upstairs-sunday-school-rooms` links the upstairs Sunday School
    rooms,
*   `visit.cgi#youth-room` links the Youth Room,
*   `visit.cgi#narthex` links the narthex,
*   `visit.cgi#nave` links the nave,
*   `visit.cgi#chapel` links the chapel,
*   `visit.cgi#library` links the library,
*   `visit.cgi#conference-room` links the conference room by the library,
*   `visit.cgi#office` links the main office,
*   `visit.cgi#bishops-assistants-office` links the bishop's assistant's office,
*   `visit.cgi#senior-pastors-office` links the senior pastor's office,
*   `visit.cgi#staff-conference-room` links the staff conference room,
*   `visit.cgi#lounge` links the Lounge,
*   `visit.cgi#scouts-room` links the Scout's room,
*   `visit.cgi#nursery` links the Nursery,
*   `visit.cgi#gym` links the gym,
*   `visit.cgi#childrens-choir-room` links the children's choir room,
*   `visit.cgi#sunday-school-rooms` links the Sunday School rooms,
*   `visit.cgi#sewing-room` links the sewing room,
*   `visit.cgi#choir-room` links the choir room,
*   `visit.cgi#music-office` links the director of music's office, and
*   `visit.cgi#old-sunday-school-rooms` links the old Sunday School rooms.

For example, a link for the location of morning worship could be written:

```
Morning Worship is in the [nave](visit.cgi#nave).
```

### Nonbreaking Spaces

If two pieces of text should be separated by a space, but should still always
appear on the same line, write `&nbsp;` (for "nonbreaking space") instead of a
space in the Markdown.  For example,

```
Evening worship will begin at 7:00&nbsp;PM.
```

prevents the `7:00` and the `PM` from being separated if there is only enough
space to fit the `7:00` at the end of the line.

See the Style Guide below for more information.

## Markdown Extensions

The website also supports some special Markdown syntax, described below.

### Paragraph Anchors

A paragraph that begins with a line of the form `{anchor:[name]}` can be linked
to by using the given name as an anchor name.  For instance, a paragraph like

```
{anchor:greeter}
The Grace Greeter is…
```

in `resources.md` can be linked to with a link like

```
[Grace Greeter (Church Newsletter)](resources.cgi#greeter)
```

### Special Content

A line of the form `{include:[name]}` all by itself is displayed as the named
special content from the `content/snippets` folder.  For example, the line

```
{include:elca_logos}
```

includes the logos for various ELCA-affiliated organizations.

A line that is just `{carousel}` all by itself is displayed as an image carousel
using images from `content/images/carousel`; a line that is just
`{upcoming_events}` all by itself is displayed as a list of links to upcoming
featured events; a line that is just `{calendar}` all by itself is displayed as
a calendar; and a line that is just `{greeters}` all by itself is displayed as a
list of current and recent greeters.

# Church Calendar

The website calendar currently shows any non-all-day events on the primary
Google calendar for `office@egrace.org`.  Any event whose name ends in
"(Featured)" will also be shown on the "Upcoming Events" list on the front page.

# Style Guide

The items below are from the style guide for the original website:

## General Style

*   Use proper spelling and grammar full sentences wherever possible.

*   Avoid exclamations.

*   Use gender-neutral language.  Do not imply a gender for God except as in the
    person of Jesus.  Example: "God's grace", not "His grace".

*   For consistency, always write "worship", not "worship service".

*   When linking to a PDF, end the link text with "(PDF)".  (Links to PDFs can
    cause accessibility issues if not properly called out.)

## Capitalization

*   Write "Lord", not "LORD".

*   Capitalize "bible" only when it refers to the scripture, not a copy of the
    scripture.  Example: "Bible reading", not "bible reading", but "new bibles",
    not "new Bibles".

*   Capitalize "Holy Communion" when referring to the sacrament.

*   Do not capitalize "baptism" or "communion", even when referring to a
    sacrament.

Punctuation
-----------

*   Do not use three periods in place of an ellipsis ("…").  Example: "See full
    calendar…", not "See full calendar...".

*   Place periods and commas that follow but are not part of a quotation after
    the quotation marks unless they can be combined with punctuation in the
    quotation.

*   Use the serial comma.  Example: "via a prayer chain, holiday gifts for
    shut-ins, and food and meals for funerals", not "via a prayer chain, holiday
    gifts for shut-ins and food and meals for funerals".

*   Do not use hyphens ("-"), which indicate compound words, in place of en
    dashes ("–"), which indicate ranges, or em dashes ("—"), which set off
    phrases.  Example: "December 17–19", not "December 17-19".

*   Do not places spaces next to hyphens or dashes.  Example: "December 17–19",
    not "December 17 – 19".

*   Write singular possessives by adding an apostrophe and an "s".  Example:
    "Jesus's", not "Jesus'".

*   Do not use curly quotes ("“", "”", "‘", and "’").  Example: "Jesus's", not
    "Jesus’s".

*   Use double quotes for quotations, single quotes for quotations in
    quotations, double quotes for quotations in quotations in quotations, etc.

*   Do not use a backslash ("\"), which can mean "without", in place of a slash
    ("/"), which usually means "or".

*   Do not use symbols other than the en dash ("–") as abbreviations.  Example:
    "quilting and sewing", not "quilting/sewing" or "quilting & sewing".

*   Use en dashes ("–") for ranges that are not parts of a sentence and whose
    endpoints consist only of digits and symbols.  Use words in all other cases.
    Example: "17–19" outside of a sentence, "17 through 19" inside a sentence,
    and "July through August" everywhere.

Abbreviations
-------------

*   Do not use contractions, except in direct quotations.  Example: "we have",
    not "we've".

*   Write initialisms in full uppercase and without dots.  Example: "PM", not
    "p.m.", and "US", not "U.S."

*   Do not use abbreviations other than acronyms, initialisms, and "etc."
    outside of titles and addresses.  Example: "meeting", not "mtg."

*   When an abbreviation appears in a name, connect it to the following word by
    a nonbreaking space (written as `&nbsp;` in the Markdown).  Example:
    "Rev.&nbsp;Jane Doe", not "Rev. Jane Doe".

*   Avoid initials in names.  If one is used, join it to any adjacent names with
    nonbreaking spaces.  Example: "Rev.&nbsp;Jane&nbsp;X.&nbsp;Doe", not
    "Rev.&nbsp;Jane X. Doe".

Numbers
-------

*   When a number attaches to a word, connect the two by a nonbreaking space
    (written as "&nbsp;" in the Markdown).  Example: "7:00&nbsp;PM", not "7:00
    PM", and "Isaiah&nbsp;61:1–4", not "Isaiah 61:1–4".

*   When two numbers in a list attach to a words, connect everything by
    nonbreaking spaces.  Example: "July&nbsp;17&nbsp;and&nbsp;19", not
    "July&nbsp;17 and 19", and "Isaiah&nbsp;61:1–4,&nbsp;8–11", not "Isaiah
    61:1–4, 8–11".

*   When three or more numbers in a list attach to a words, connect the first by
    a nonbreaking space, join the "and" and the last number with a nonbreaking
    spaces, and use plain spaces elsewhere.  Example: "July&nbsp;17, 19,
    and&nbsp;21", not "July 17, 19, and 21".

*   When a number comes at the end of a sentence, precede it with a nonbreaking
    space.

*   Write dates without years as the month name in full, a nonbreaking space,
    and the day.  Example: "July&nbsp;17", not "7/17".

*   Write times as the hour, a colon, the minutes, and an AM or PM suffix
    attached by a nonbreaking space.  (However, omit the AM or PM suffix if the
    time is accompanied by a phrase like "in the morning" or "in the evening".)
    Example: "4:00&nbsp;PM", not "4:00", "four", or "4".

*   Write US phone numbers as an area code in parentheses, a nonbreaking space,
    the three-digit prefix, a hyphen (`-`), and the four-digit suffix.  Example:
    "(402)&nbsp;474-1505", not "402-474-1505".

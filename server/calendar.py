#! /usr/bin/env python3

import os
import pickle

import re

from uuid import uuid5, NAMESPACE_DNS

from datetime import datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Constants and Utility

NONANCHOR_CHARACTERS = re.compile(r'\W+')


def make_anchor(string):
    return NONANCHOR_CHARACTERS.sub('-', string.lower())


NAMESPACE = uuid5(NAMESPACE_DNS, 'egrace.org')


REFERENCE_TIME = datetime.now().astimezone()


CENTRAL_TIME = timezone('US/Central')


# Event Class

class Event:
    def __init__(self, name, start, end, location, notes):
        self.name = name
        self.start = start
        self.end = end
        self.location = location if location is not None else ''
        self.notes = notes if notes is not None else ''
        self.uuid = uuid5(NAMESPACE, f'{name}-{start}-{end}-{location}-{notes}')
        if start.year != REFERENCE_TIME.year or start.month != REFERENCE_TIME.month or start >= REFERENCE_TIME:
            self.anchor = make_anchor(name)
        else:
            self.anchor = None
        if start.strftime('%p') == end.strftime('%p'):
            self.times = f'{start.strftime("%-I:%M")}–{end.strftime("%-I:%M&nbsp;%p")}'
        else:
            self.times = f'{start.strftime("%-I:%M&nbsp;%p")}–{end.strftime("%-I:%M&nbsp;%p")}'
        if location:
            self.comma_location = f', {location}'
        else:
            self.comma_location = ''


# Event Loading

_CREDENTIALS_PATH = '/home/elcagrace/credentials.json'
_CREDENTIAL_SCOPES = ('https://www.googleapis.com/auth/calendar.readonly',)
_TOKEN_PATH = '/home/elcagrace/token.pickle'


def get_credentials():
    credentials = None
    if os.path.exists(_TOKEN_PATH):
        with open(_TOKEN_PATH, 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # do not uncomment on the server
            # flow = InstalledAppFlow.from_client_secrets_file(_CREDENTIALS_PATH, _CREDENTIAL_SCOPES)
            # credentials = flow.run_local_server()
            pass
        with open(_TOKEN_PATH, 'wb') as token:
            pickle.dump(credentials, token)
    return credentials


_CALENDAR_SERVICE = None


def get_calendar_service():
    global _CALENDAR_SERVICE
    if _CALENDAR_SERVICE is None:
        _CALENDAR_SERVICE = build('calendar', 'v3', credentials=get_credentials())
    return _CALENDAR_SERVICE


def get_events(minimum, maximum, pattern=None):
    records = get_calendar_service().events().list(
        calendarId='primary',
        timeMin=minimum.isoformat(),
        timeMax=maximum.isoformat(),
        singleEvents=True,
        orderBy='startTime',
    ).execute().get('items', [])
    results = []
    for record in records:
        name = record['summary']
        if pattern is None or pattern.fullmatch(name):
            start = record['start'].get('dateTime')
            end = record['end'].get('dateTime')
            if start is not None and end is not None:
                location = record.get('location')
                notes = record.get('notes')
                results.append(Event(name, parse(start), parse(end), location, notes))
    return results


def get_events_by_horizon(days, pattern=None):
    minimum = datetime.now().astimezone(CENTRAL_TIME)
    maximum = minimum + relativedelta(days=days)
    return get_events(minimum, maximum, pattern)


def get_events_by_month(year, month, pattern=None):
    minimum = CENTRAL_TIME.localize(datetime(year, month, 1))
    maximum = CENTRAL_TIME.localize(datetime(year, month, 1) + relativedelta(months=1))
    return get_events(minimum, maximum, pattern)


# Event Templates

def load_calendar_template(name):
    with open(f'theme/templates/calendar/{name}.html', encoding='utf-8') as template_file:
        return template_file.read()


CALENDAR_TEMPLATE = load_calendar_template('calendar')
DAY_TEMPLATE = load_calendar_template('day')
EVENT_TEMPLATE = load_calendar_template('event')
EXPANDED_EVENT_TEMPLATE = load_calendar_template('expanded_event')


# Calendar Formatting


def format_event(event):
    return EVENT_TEMPLATE.format(
        uuid=event.uuid,
        name=event.name,
        times=event.times,
        comma_location=event.comma_location,
        anchor_attribute=f'id="{event.anchor}"' if event.anchor is not None else '',
    ), EXPANDED_EVENT_TEMPLATE.format(
        uuid=event.uuid,
        name=event.name,
        times=event.times,
        date=event.start.strftime('%B %-d, %Y'),
        location=event.location,
        notes=event.notes,
    )


def format_day(year, month, day, events):
    start = CENTRAL_TIME.localize(datetime(year, month, day))
    end = CENTRAL_TIME.localize(datetime(year, month, day) + relativedelta(days=1))
    formatted_events = tuple(format_event(event) for event in events if start <= event.start < end)
    return DAY_TEMPLATE.format(
        year=year,
        month=month,
        day=day,
        events=''.join(event for event, _ in formatted_events),
    ), '\n'.join(expanded_event for _, expanded_event in formatted_events)


def format_calendar(year, month):
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    events = get_events_by_month(year, month)
    current_month = datetime(year, month, 1)
    previous_month = current_month - relativedelta(months=1)
    next_month = current_month + relativedelta(months=1)
    days = '<tr>'
    fill = (current_month.weekday() + 1) % 7
    for _ in range(fill):
        days += '<td></td>'
    expansions = ''
    for day in range(1, 32):
        try:
            unexpanded_day, expanded_day = format_day(year, month, day, events)
        except ValueError:
            break
        days += unexpanded_day
        expansions += expanded_day
        fill += 1
        if fill >= 7:
            days += '</tr><tr>'
            fill = 0
    for _ in range((7 - fill) % 7):
        days += '<td></td>'
    days += '</tr>'
    return CALENDAR_TEMPLATE.format(
        year_of_current_month=current_month.strftime('%Y'),
        name_of_current_month=current_month.strftime('%B'),
        year_of_previous_month=previous_month.strftime('%Y'),
        previous_month = previous_month.strftime('%m'),
        year_of_next_month=next_month.strftime('%Y'),
        next_month = next_month.strftime('%m'),
        days=days,
        expansions=expansions,
    )

# License: none (public domain)

import datetime
import dateutil.parser
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import file


class GoogleCalendar(object):
    """Simple object for interacting with Google Calendar API."""

    def __init__(self, credentials_filename):
        """Creates Google Calendar API interface using the given credentials."""
        storage = file.Storage(credentials_filename)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            raise Exception('Credentials invalid or missing :(')
        http = httplib2.Http()
        http = credentials.authorize(http)
        self.service = discovery.build('calendar', 'v3', http=http)


    def insert_event(self, calid, summary, startdt, enddt, timezone):
        """Inserts a new calendar event."""
        newevent = {
            'summary': summary,
            'start': {
                'dateTime': startdt.isoformat(),
                'timeZone': timezone
            },
            'end': {
                'dateTime': enddt.isoformat(),
                'timeZone': timezone
            }
        }
        self.service.events().insert(calendarId=calid, body=newevent).execute()


    def events(self, calid):
        """Gets the list of calendar events."""
        page_token = None
        events = []
        while True:
            event_list = self.service.events().list(calendarId=calid, pageToken=None).execute()
            events.extend(event_list['items'])
            page_token = event_list.get('nextPageToken')
            if not page_token:
                break
        return events


    def calendar_list(self):
        """Gets lits of google calendars."""
        page_token = None
        calendars = []
        while True:
            calendar_list = self.service.calendarList().list(pageToken=None).execute()
            calendars.extend(calendar_list['items'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return calendars
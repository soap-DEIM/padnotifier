from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

import httplib2
import parse
import pytz
import datetime

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id='792502215934.apps.googleusercontent.com',
    client_secret='NJtj6GWMtLGCbQSvTLCbEuJ9',
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='Limited Dungeon Alarm')

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid is True:
    credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google APIs Console
# to get a developerKey for your own application.
service = build(serviceName='calendar', version='v3', http=http,
                developerKey='AIzaSyBedS4x3i-cBdVfhtAVfywgq8Z7WLuacqM')

calendarId = 'coder.soap@gmail.com'


def newTime(today, hour):
    tz = pytz.timezone('US/Pacific')
    dtm = datetime.datetime.now(tz)
    d = dtm.date()
    if today is False:
        d += datetime.timedelta(days=1)
    if hour == 24:
        d += datetime.timedelta(days=1)
        hour = 0
    dt = datetime.datetime(
        year=d.year,
        month=d.month,
        day=d.day,
        hour=hour)
    return str(dt.date()) + 'T' + str(dt.time()) + '.000-07:00'


'''
colorId value
'11':red

'''


def newEvent(today, hour):
    start = newTime(today, hour)
    end = newTime(today, hour + 1)
    print "start time: ", start
    print "end time: ", end
    event = {
        'summary': 'Call of Limited Dungeon',
        'location': 'PAD',
        'start': {
            'dateTime': start,
            },
        'end': {
            'dateTime': end,
            },
        'colorId': '11',
        }
    return event


def getEvents(pageToken=None):
    events = service.events().list(
        calendarId=calendarId,
        singleEvents=True,
        maxResults=100,
        orderBy='startTime',
        timeMin='2012-11-01T00:00:00-08:00',
        timeMax='2013-11-30T00:00:00-08:00',
        pageToken=pageToken,
        ).execute()
    return events


def insertEvents(event):
    created_event = service.events().insert(
        calendarId=calendarId,
        body=event).execute()
    return created_event


def main():
    for i in parse.event_time_today:
        event = newEvent(True, int(i))
        insertEvents(event)

    for i in parse.event_time_tomorrow:
        event = newEvent(False, int(i))
        insertEvents(event)
'''
    events = getEvents()
    while True:
        for event in events['items']:
            pprint.pprint(event)
        page_token = events.get('nextPageToken')
        if page_token:
            events = getEvents(page_token)
        else:
            break
'''

if __name__ == '__main__':
    main()

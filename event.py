# Google client API #
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

# Common python modules #
import json
import httplib2
import pytz
import datetime

# private modules #
import parse


# load configure file
config = open('userconf.json').read()
config_data = json.loads(config)

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret are copied from the API Access tab on
# the Google APIs Console
FLOW = OAuth2WebServerFlow(
    client_id=config_data['client_id'],
    client_secret=config_data['client_secret'],
    scope=config_data['scope'],
    user_agent=config_data['user_agent'])

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
                developerKey=config_data['developerKey'])

calendarId = 'coder.soap@gmail.com'


# @newTime
# @today [bool] : indicates today or tomorrow
# @hour  [int]  : the hour of time
# returns time info of format "yyyy-mm-ddThh:mm:ss.000%p"
# which compliance to Google API
# here we use fixed timezone PDT so %p is -07:00
def newTime(today, hour):
    # news that www.puzzledragonx.com announced
    # use time in timezone PDT, a.k.a. US/Pacific
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


# @newEvent
# @today [bool] : indicates today or tomorrow
# @hour  [int]  : the hour of time
# returns a event constructed of provided time info
# we are supposed to update daily so only hour is required
# TODO
# support event of variable format
def newEvent(today, hour):
    start = newTime(today, hour)
    end = newTime(today, hour + 1)
    # debug #
    print "[DEBUG] start time: ", start
    print "[DEBUG] end time: ", end
    # end debug #
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


# @insertEvent
# @event [event] : event to insert
# insert event to Google calendar
# for complete event definition please refer to
# https://developers.google.com/google-apps/calendar/v3/reference/events
def insertEvent(event):
    created_event = service.events().insert(
        calendarId=calendarId,
        body=event).execute()
    return created_event


def main():
    for i in parse.event_time_today:
        event = newEvent(True, int(i))
        insertEvent(event)

    for i in parse.event_time_tomorrow:
        event = newEvent(False, int(i))
        insertEvent(event)

if __name__ == '__main__':
    main()

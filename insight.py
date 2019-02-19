import requests
import urllib
from contextlib import closing
import csv
from collections import namedtuple

from datetime import datetime
from datetime import timedelta
import os
import pytz

local_timezone = pytz.timezone(os.environ["TIMEZONE"])


LOGIN_URL = "https://profile.insighttimer.com/profile_signin/request"
INSIGHT_CSV_URL = "https://profile.insighttimer.com/sessions/export"

Entry = namedtuple('Entry', ['duration', 'activity', 'start_datetime', 'preset'])

def get_insight_data(username, password):
    values = {'user_session[email]' : username,
              'user_session[password]' : password }
    login_data = urllib.parse.urlencode(values)

    # Start a session so we can have persistent cookies
    session = requests.session()
    #logger.debug("Submitting POST request to insighttimer.com...")
    r = session.post(LOGIN_URL, data=login_data)
    #logger.debug("Submitting GET request to insighttimer.com...")
    r = session.get(INSIGHT_CSV_URL)
    decoded_content = r.content.decode('utf-8')
    print(decoded_content)

    return csv.DictReader(decoded_content.splitlines(), delimiter=',')

def timedelta_from_hh_mm_ss(s):
  t = datetime.strptime(s,"%H:%M:%S")
  return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
  
def process_insight_datapoint(row):
  # Expects a dictionary of CSV data from insight timer
  duration = timedelta_from_hh_mm_ss(row['Duration'])
  start_datetime = pytz.utc.localize(datetime.strptime(row['StartedAt (UTC)'],
                                            '%m/%d/%Y %H:%M:%S'))
  return Entry(duration=duration,
               activity=row['Activity'],
               start_datetime=start_datetime,
               preset=row['Preset'])

def get_todays_meditation_duration(username, password):
  data = [process_insight_datapoint(row) for row in get_insight_data(username, password)]
  today = local_timezone.localize(datetime.now()).date()
  print(data)
  
  filtered_activities = [entry for entry in data if "meditation" in entry.activity.lower()]
  
  return sum((entry.duration for entry in filtered_activities if entry.start_datetime.date() == today),
             timedelta())

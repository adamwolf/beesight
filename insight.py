import requests
import urllib
from contextlib import closing
import csv

LOGIN_URL = "https://insighttimer.com/user_session"
INSIGHT_CSV_URL = "https://insighttimer.com/sessions/export"

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

    return csv.DictReader(decoded_content.splitlines(), delimiter=',')

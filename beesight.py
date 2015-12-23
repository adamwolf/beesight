import configparser
import datetime
import urllib
import requests
import sys
import json
import time

# complain on config file issues
# complain on bad login
# don't hardcode timezone to japan

CONFIG_FILE_NAME = 'config.ini'
INSIGHT_SECTION = 'insight'
BEEMINDER_SECTION = 'beeminder'

LOGIN_URL = "https://insighttimer.com/user_session"
INSIGHT_CSV_URL = "https://insighttimer.com/users/export"

BASE_URL= "https://www.beeminder.com/api/v1/"
GET_DATAPOINTS_URL = BASE_URL + "users/%s/goals/%s/datapoints.json?auth_token=%s"
POST_MANY_DATAPOINTS_URL = BASE_URL + "users/%s/goals/%s/datapoints/create_all.json?auth_token=%s"
POST_DATAPOINTS_URL = GET_DATAPOINTS_URL + "&timestamp=%s&value=%s&comment=%s"

def get_insight_data():
    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE_NAME)

    username = config.get(INSIGHT_SECTION, "username")
    password = config.get(INSIGHT_SECTION, "password")

    values = {'user_session[email]' : username,
              'user_session[password]' : password }
    login_data = urllib.parse.urlencode(values)

    # Start a session so we can have persistent cookies
    session = requests.session()
    r = session.post(LOGIN_URL, data=login_data)
    r = session.get(INSIGHT_CSV_URL)
    return r.text.split('\n')

def post_beeminder_entry(entry):
        config = configparser.RawConfigParser()
        config.read(CONFIG_FILE_NAME)

        username = config.get(BEEMINDER_SECTION, "username")
        auth_token = config.get(BEEMINDER_SECTION, "auth_token")
        goal_name = config.get(BEEMINDER_SECTION, "goal_name")

        session = requests.session()
        full_url = POST_DATAPOINTS_URL % (username, goal_name, auth_token, entry["timestamp"], entry["value"], entry["comment"])
        r = session.post(full_url)

        print ("Posted entry: ", r.text)

def get_beeminder():
        config = configparser.RawConfigParser()
        config.read(CONFIG_FILE_NAME)

        username = config.get(BEEMINDER_SECTION, "username")
        auth_token = config.get(BEEMINDER_SECTION, "auth_token")
        goal_name = config.get(BEEMINDER_SECTION, "goal_name")

        response = urllib2.urlopen(GET_DATAPOINTS_URL % (username, goal_name, auth_token))
        the_page = response.read()
        return the_page

def beeminder_to_one_per_day(beeminder_output):
    bm = json.loads(beeminder_output)

    s = {}

    # skip first two header lines
    for entry in bm:
        ts = entry['timestamp']
        dt = datetime.datetime.fromtimestamp(ts)

        # need to move back one dayfrom the beeminder time, because it
        # pushes the day forward to 01:00 on day + 1, at least in JST
        d = dt.date() - datetime.timedelta(days=1)

        if not d in s:
            s[d] = 1

    return s.keys()

def csv_to_todays_minutes(csv_lines):
    minutes = int(0)

    # skip first two header lines
    for l in csv_lines[2:6]:
        line = l.split(",")
        print (line[0])
        datetime_part = line[0]
        minutes_entry = line[1]
        date_part = datetime_part.split(" ")[0]
        date_parts = date_part.split("/")
        if len(date_parts) == 3:
            m, d, y = map(int, date_parts)
            dt = datetime.date(y, m, d)

            if dt == datetime.date.today():
                minutes += int(minutes_entry)

    return minutes	
	
def date_to_jp_timestamp(dt):
    d = datetime.datetime.combine(dt, datetime.time())
    return int(time.mktime(d.timetuple()))

if __name__ == "__main__":
    # get today's minutes from insight
    insight_minutes = csv_to_todays_minutes(get_insight_data())
    if insight_minutes == 0:
        print ("No minutes logged for today's date on InsightTimer.com")
        sys.exit()
    else:
        print (insight_minutes, " minutes meditated today according to InsightTimer.com")

    # get dates of days meditated, from beeminder
    #beeminder_dates = beeminder_to_one_per_day(get_beeminder())
    #print "%s datapoints in beeminder" % len(beeminder_dates)

    # get today's date
    new_date = datetime.date.today()

    # create beeminder-friendly datapoints
    new_datapoint = {'timestamp': date_to_jp_timestamp(new_date), 'value':insight_minutes, 'comment':"beesight+script+entry"}

    print (insight_minutes, " minutes to post")

    post_beeminder_entry(new_datapoint)

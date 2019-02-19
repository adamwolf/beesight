from flask import Flask, request
import os
import pytz
from datetime import datetime, timedelta

from beeminder import upload_to_beeminder, get_last_datapoint
from insight import get_todays_meditation_duration, get_insight_data, process_insight_datapoint                                 

for var in ["BEEMINDER_USERNAME",
            "BEEMINDER_AUTH_TOKEN",
            "BEEMINDER_GOAL",
            "INSIGHT_USERNAME",
            "INSIGHT_PASSWORD",
            "TIMEZONE",]:
  if var not in os.environ:
    raise Exception("Please define {} in the .env file.".format(var))

app = Flask(__name__, static_folder='views')

local_timezone = pytz.timezone(os.environ["TIMEZONE"])

def upload_todays_meditation_duration():
  goal_name = os.environ['BEEMINDER_GOAL']
  duration = get_todays_meditation_duration(os.environ["INSIGHT_USERNAME"], os.environ["INSIGHT_PASSWORD"])
  if not duration:
    return
  last_datapoint = get_last_datapoint(goal_name)
  last_datapoint_day = datetime.strptime(last_datapoint['daystamp'], "%Y%m%d")
  last_datapoint_duration = timedelta(hours=last_datapoint['value'])
                      
  now = datetime.now(local_timezone)
  if now.date() == last_datapoint_day.date():
    print("The last datapoint was from today.")
    # check to see if its the same value
    if duration - timedelta(seconds=0.5) < last_datapoint_duration < duration + timedelta(seconds=0.5):
      print("The last datapoint for today, {}, was within 1 second of what we wanted to post({}), so we're skipping the update.".format(last_datapoint_duration, duration))
      return
    else:
      print("The last datapoint for today varied from the current one by : {}".format(duration - last_datapoint_duration))
  else:
    print("The last datapoint was not from today.")

  upload_to_beeminder(goal_name, str(duration))
  
@app.route("/update", methods=["POST"])
def got_poked_by_beeminder():
  if request.values['username'] != os.environ['BEEMINDER_USERNAME']:
    print("Not for me: ", request.values['username'])
    abort(403)
  else:
    upload_todays_meditation_duration()
    return "success"

@app.route("/")
def main():
  return "hullo"

if __name__ == "__main__":
  app.run()
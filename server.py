from flask import Flask, request
import os

from beeminder import upload_to_beeminder
from insight import get_todays_meditation_duration                                          

for var in ["BEEMINDER_USERNAME",
            "BEEMINDER_AUTH_TOKEN",
            "BEEMINDER_GOAL",
            "INSIGHT_USERNAME",
            "INSIGHT_PASSWORD",
            "TIMEZONE",]:
  if var not in os.environ:
    raise Exception("Please define {} in the .env file.".format(var))

app = Flask(__name__, static_folder='views')

@app.route("/update", methods=["POST"])
def got_poked_by_beeminder():
  if request.values['username'] != os.environ['BEEMINDER_USERNAME']:
    print("Not for me: ", request.values['username'])
    abort(403)
  else:
    goal_name = os.environ['BEEMINDER_GOAL']
    duration = str(get_todays_meditation_duration(os.environ["INSIGHT_USERNAME"], os.environ["INSIGHT_PASSWORD"]))
    upload_to_beeminder(goal_name, duration)
    return "success"

@app.route("/")
def main():
  return "hullo"

if __name__ == "__main__":
  app.run()
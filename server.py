import sys
import platform

from flask import Flask, send_from_directory, jsonify, request, abort
import os
import logging
import requests
import sys
import time
from datetime import datetime
import pytz

import insight


for var in ["BEEMINDER_USERNAME",
            "BEEMINDER_AUTH_TOKEN",
            "BEEMINDER_GOAL",
            "INSIGHT_USERNAME",
            "INSIGHT_PASSWORD",
            "TIMEZONE",]:
  if var not in os.environ:
    raise Exception("Please define {} in the .env file.".format(var))

timezone = pytz.timezone(os.environ["TIMEZONE"])

app = Flask(__name__, static_folder='views')

  
@app.route("/")
def main():
  print(insight.get_insight_data(os.environ["INSIGHT_USERNAME"], 
                                 os.environ["INSIGHT_PASSWORD"]))
  return "hullo"


if __name__ == "__main__":
  app.run()
beesight.py - minutes fork by bluremi
-------------
This is a small script which retrieves meditation data from insighttimer.com and posts the data points to your beeminder goal, so that you can easily track how often you're meditating.

The original script by Dave Cahill (https://github.com/davecahill/beesight) just recorded whether a day was a hit or a miss. This version records how many minutes in total you've meditated today. It supports multiple sessions in one day.

It is intended to be run every evening as a scheduled task, picking up new datapoints and posting them to beeminder.

Prerequisites
--------------
Python version 3.5 or later
Use pip35.exe to download the "requests" package (pip35.exe install requests)

Usage
---------

Rename default_config.ini to config.ini and fill in your insighttimer.com and beeminder credentials.

Your beeminder auth token can be found at this URL when logged in:
https://www.beeminder.com/api/v1/auth_token.json

To run:
```
python beesight.py
```

To schedule as a Windows task, the action should launch python.exe with the path to the script as an argument.

Notes
------
This script will only retrieve today's minutes. If you want to post yesterday's minutes that is currently unsupported.

If you run the script more than once it will post duplicate entries.


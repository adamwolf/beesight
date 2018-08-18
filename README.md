beesight.py - minutes fork by bluremi
-------------
This is a small script which retrieves meditation data from insighttimer.com and posts the data points to your beeminder goal, so that you can easily track how often you're meditating.

The original script by Dave Cahill (https://github.com/davecahill/beesight) just recorded whether a day was a hit or a miss. This version records how many minutes in total you've meditated today. It supports multiple sessions in one day.

It is intended to be run every evening as a scheduled task, picking up new datapoints and posting them to beeminder.

Prerequisites
--------------
Python version 3.5 or later
Use pip35.exe to download the "requests" package, e.g. from the command prompt run:
```
pip35.exe install requests
```
Usage
---------

- Rename default_config.ini to config.ini and fill in your insighttimer.com and beeminder credentials. If you are in a different timezone than EST,
  update the utc_timezone parameter (e.g. Pacific Time would be "-8").

- Your beeminder auth token can be found at this URL when logged in:

https://www.beeminder.com/api/v1/auth_token.json

- To run:
```
python beesight.py
```

- To schedule as a Windows task, the action should launch python.exe with the path to the script as an argument.

Notes
------
This script will only retrieve today's minutes. If you want to post yesterday's minutes that is currently unsupported.

It also only posts minutes for log entries containing the word "Meditation". 

If you run the script more than once it will post duplicate entries.

Change Log
------
2018-08-18: Updated to be compatible with changed Insight Timer log format that uses hh:mm:ss instead of just minutes in the duration part.
2016-02-02: Merged Josh Curtis fork. Bug fixes:
            - Timezone correction now works on the 1st of the month
			- Script will now gracefully handle data where there are fewer than 4 sessions recorded.
2016-01-28: Timezone correction added by Josh Curtis in new fork.
2016-01-13: Updated insighttimer.com session URL (script was broken by server-side changes)
2015-12-28: Added logging output
2015-12-23: First fork released, records session minutes.


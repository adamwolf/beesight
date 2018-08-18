Beemind Insight Timer
---------------------

This is a work-in-progress refactor/rewrite of beesight.py to make this suitable for Glitch.

The first milestone is for it to have your total minutes of meditation per day posted.  It won't be smart about duplicates or anything, so make sure to set your aggday to something like "last".

The goal should be in hours.

It only looks for things with the word meditation in the activity name.

It would be better if it was smarter!

* I would prefer if it put one entry per entry, rather than summing the entries, but that's trickier for an initial implementation.
* Maybe, if it's fun, think about how to handle meditation over the deadline/midnight.
* Maybe, if it's fun, turn process_insight_data into a generator of some sort
 
I keep forgetting how to setup integration with Beeminder.  Go to https://www.beeminder.com/settings/account#account-permissions, and register a new app.  Set the Autofetch Callback URL to the update URL here.  When Beeminder wants to grab a datapoint, or when you hit Refresh on a goal, Beeminder will POST to that Autofetch Callback URL.  It posts the goal name and the username, and some other things I think.  See the API docs for details.  Then, do something like `curl -X PUT https://www.beeminder.com/api/v1/users/your_username/goals/goalname -d auth_token=xxxxxx -d datasource=your_api_name` 
History
-------
Originally by Dave Cahill (https://github.com/davecahill/beesight) 
Updated by bluremi (https://github.com/benkloester/beesight)
Modified by Adam Wolf 

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


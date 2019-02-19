import requests
import os

def upload_to_beeminder(goal_name, val, comment=None):
  data = {"value": val,
          "auth_token": os.environ['BEEMINDER_AUTH_TOKEN']}
  
  if comment:
    data['comment'] = comment
  
  url = "https://www.beeminder.com/api/v1/users/{0}/goals/{1}/datapoints.json".format(os.environ["BEEMINDER_USERNAME"],
                                                                                      goal_name)
  r = requests.post(url, json=data)
  if not r.status_code == requests.codes.ok:
    print(r.status_code, r.text)
    raise
    
def get_last_datapoint(goal_name):
    url = "https://www.beeminder.com/api/v1/users/{0}/goals/{1}".format(os.environ["BEEMINDER_USERNAME"],
                                                                                      goal_name)
    print(url)
    r = requests.get(url, params={'auth_token': os.environ['BEEMINDER_AUTH_TOKEN']})
    if not r.status_code == requests.codes.ok:
      print(r.status_code, r.text)
      raise
    
    return r.json()['last_datapoint']
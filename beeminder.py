import requests

def upload_to_beeminder(username, goal_name, val, comment=None):
  data = {"value": val,
          "auth_token": os.environ['BEEMINDER_AUTH_TOKEN']}
  
  if comment:
    data['comment'] = comment
  
  url = "https://www.beeminder.com/api/v1/users/{0}/goals/{1}/datapoints.json".format(username,
                                                                                      goal_name)
  r = requests.post(url, json=data)
  if not r.status_code == requests.codes.ok:
    print(r.status_code, r.text)
    raise
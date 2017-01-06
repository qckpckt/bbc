import os
import requests
import datetime

BAMBOO_TOKEN = os.getenv('BAMBOO_API_KEY')
DEFAULT_HEADERS = {'Accept': 'application/json'}
META_URL = 'https://api.bamboohr.com/api/gateway.php/mobify/v1/meta/fields/'
CHANGED_SINCE_API = 'https://api.bamboohr.com/api/gateway.php/mobify/v1/employees/changed/?since={timestamp}&type=inserted'


def whats_new():

    last_run = datetime.datetime.now() - datetime.timedelta(weeks=2)
    time_stamp = str(last_run.isoformat()).split('.')[0]
    date_plus_timezone = time_stamp + '-08.00'
    url = CHANGED_SINCE_API.format(timestamp = date_plus_timezone)
    auth = requests.auth.HTTPBasicAuth(BAMBOO_TOKEN, 'x')
    resp = requests.get(url, auth=auth, headers = DEFAULT_HEADERS)
    directory = resp.json()
    return directory['employees']

if __name__ == '__main__':
    whats_new()

# import pdb; pdb.set_trace()

import os
import requests
import datetime
import signature
from util import export_to_csv

BAMBOO_TOKEN = os.getenv('BAMBOO_API_KEY')
DEFAULT_HEADERS = {'Accept': 'application/json'}
META_URL = 'https://api.bamboohr.com/api/gateway.php/mobify/v1/meta/fields/'
CHANGED_SINCE_API = 'https://api.bamboohr.com/api/gateway.php/mobify/v1/employees/changed/?since={timestamp}&type=updated'


def whats_new():

    last_run = datetime.datetime.now() - datetime.timedelta(weeks=2)
    time_stamp = str(last_run.isoformat()).split('.')[0]
    date_plus_timezone = time_stamp + '-08:00'
    url = CHANGED_SINCE_API.format(timestamp = date_plus_timezone)
    auth = requests.auth.HTTPBasicAuth(BAMBOO_TOKEN, 'x')
    resp = requests.get(url, auth=auth, headers = DEFAULT_HEADERS)
    directory = resp.json()
    return directory['employees']

# def first(iterator, condition=None):
#     # lambda function used above in finding specific users
#     condition = (condition or (lambda x: True))
#     return next ((x for x in iterator if condition(x)))


if __name__ == '__main__':
    updated_ids = whats_new()
    directory = signature.get_bamboo_directory()
    filtered_directory = []
    mobifyers = []
    for user in updated_ids:
        for employee in directory:
            if user == employee['id']:
                filtered_directory.append(employee)
    for employee in filtered_directory:
        new_employee = signature.Mobifyer(employee)
        mobifyers.append(new_employee.__dict__())

    export_to_csv(mobifyers, 'mycsv.csv')

    signature.gam_cmd()

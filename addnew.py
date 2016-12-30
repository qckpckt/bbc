import os
import requests

DEFAULT_HEADERS = {'Accept': 'application/json'}
META_URL = 'https://api.bamboohr.com/api/gateway.php/mobify/v1/meta/fields/'
CHANGED_SINCE = 'https://api.bamboohr.com/api/gateway.php/mobify/v1/employees/changed/?since={timestamp}&type=inserted'

token = os.getenv('BAMBOO_API_KEY')

auth = requests.auth.HTTPBasicAuth(token, 'x')
resp = requests.get(USE_CELL.format(employee_id=ALEX_ID), auth=auth, headers = DEFAULT_HEADERS)

# reply = resp.json()

# import pdb; pdb.set_trace()

import requests,urllib2
import json


data = {'test':'hello'}
url = "http://192.168.56.101:8080/api/v1/test/"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
print r
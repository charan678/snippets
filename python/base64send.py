import request

import urrlib2 

import urllib2, base64, json
username, password = "", ""


login_user = ""
login_passsword = ""

base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

header = {"Authorization": "Basic %s" % base64string, "App-id": "1_dpi","HTTP_REQUEST_SOURCE":"IOS", 
          "Api-user":base64.b64encode(username), "Api-pass": base64.b64encode(password), 
          'Content-Type': 'application/json'}


basetest_values = {}


localhost_url = 'https://api/v1/customer_id/'

def base64test():
    
    
    request = urllib2.Request(url, json.dumps(basetest_values), headers = header)
    response = urllib2.urlopen(request)
    result_data = response.read()
    print result_data

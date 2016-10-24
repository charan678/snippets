import request

import urrlib2 

import urllib2, base64, json
username, password = "3_4_meraaspm", "Meraas@123"


login_user = "kgopiaris@gmail.com"
login_passsword = "Meraas@1234"

base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')

header = {"Authorization": "Basic %s" % base64string, "App-id": "1_dpi","HTTP_REQUEST_SOURCE":"IOS", 
          "Api-user":base64.b64encode(username), "Api-pass": base64.b64encode(password), 
          'Content-Type': 'application/json'}


basetest_values = {"id_country_code":"AL","":"","id_number":"A998877","is_active":"1","id_typeid":"1","expiry_date":"21-07-2018","customer_id":"29","csrfmiddlewaretoken":"pSaCAxrWYzuWzOOtl39Qg0ay5ek9Alme"}


localhost_url = 'https://52.27.59.142:8005/api/v1/customer_id/'

def base64test():
    
    
    request = urllib2.Request(url, json.dumps(basetest_values), headers = header)
    response = urllib2.urlopen(request)
    result_data = response.read()
    print result_data

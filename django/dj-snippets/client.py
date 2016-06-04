import urllib2, base64, json

base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
header = {"Authorization": "Basic %s" % base64string,  
          "Api-user":base64.b64encode(username), "Api-pass": base64.b64encode(password), 
          'Content-Type': 'application/json'}


localhost_url = 'http://localhost:8000'

def test():
    url = localhost_url+'/test/'
    request = urllib2.Request(url, json.dumps(spend_values), headers = header)
    response = urllib2.urlopen(request)
    result_data = response.read()

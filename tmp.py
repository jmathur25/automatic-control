import requests
string = 'right-90'

url = 'http://192.168.4.1:80/'

request = requests.post(url, data=string)

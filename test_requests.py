import requests
URL= "https://oo648zkpsj.execute-api.us-east-1.amazonaws.com/txt2gest/I%20came%20here%20to%20live%20peacefully"
PARAMS={}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
print(data)

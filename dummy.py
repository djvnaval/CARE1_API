import requests

payload = {'page': 2, 'count': 25}
r = requests.get('https://httpbin.org/get', params=payload)

print(r.text, type(r.text))
print(r.json(), type(r.json()))     
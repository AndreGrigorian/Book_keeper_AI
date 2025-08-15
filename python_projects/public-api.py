import requests
import pprint

url = 'https://api.waifu.im/search'
params = {
    'included_tags': ['selfies'],
    'height': '>=2000'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    pprint.pprint(data)
    print(data['images'][0]['url'])
    # Process the response data as needed
else:
    print('Request failed with status code:', response.status_code)

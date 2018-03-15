import urllib.parse
import requests
import json

people_api = ('https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch=?')

# Enter the name of the artist
user_input = input('name ')

url = people_api + urllib.parse.urlencode({'user_input': user_input})
# print(url)
json_data = requests.get(url).json()

print(json_data)
# prinDict = dict(map(int, x.split(':')) for x in json_data)
# for key in json_data:
#     print(key)

# with open('people_data', 'w') as f:
#     data = j

# Extract elements from the response.

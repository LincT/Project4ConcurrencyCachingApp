import urllib.parse
from PIL import Image
import requests
import json
from pprint import pprint

# Make an api request
people_api = 'https://en.wikipedia.org/w/api.php?action=query&format=json&'

user_input = input('name: ')
# name = input('name: ')
url = people_api + urllib.parse.urlencode({'titles': user_input, 'prop': 'images'})
# print(url)
json_data = requests.get(url).json()
# pprint(json_data)

# Extract pageid from request response.
id = next(iter(json_data['query']['pages'].keys()))

# Use the pageid to get the pages and get image files
files = json_data['query']['pages'][id]['images']
# pprint(file_list)

# Get image files and put them in a list
file_list = []
for file in files:
    file_list.append(file['title'])


# Trim the 'File:' part of the image tilte
file_list = list(map(lambda each:each.strip("File:"), file_list))

# Request the image url
new_url = people_api + urllib.parse.urlencode({'titles': "Image:" + file_list[5], 'prop': 'imageinfo', 'iiprop': 'url'})
image_json_data = requests.get(new_url).json()
pprint(image_json_data)

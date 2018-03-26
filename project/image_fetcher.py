import urllib.parse
import requests



class image_fetcher():

    def fetch(self, artist):
        # Make an api request
        people_api = 'https://en.wikipedia.org/w/api.php?action=query&format=json&'

        artist = artist.title()

        # name = input('name: ')
        url = people_api + urllib.parse.urlencode({'titles': artist, 'prop': 'images'})
        json_data = requests.get(url).json()
        print(json_data)

        # Extract pageid from request response.
        try:
            page_id = next(iter(json_data['query']['pages'].keys()))

            # Use the pageid to get the pages and get image files
            files = json_data['query']['pages'][page_id]['images']

            # Get image files and put them in a list
            file_list = []
            for file in files:
                file_list.append(file['title'])

            # Trim the 'File:' part of the image tilte
            file_list = list(map(lambda each: each.strip("File:"), file_list))
            print(file_list)
            # Request the image url
            new = 2
            for n in range(len(file_list)):

                new_url = people_api + urllib.parse.urlencode({'titles': "Image:" + file_list[n], 'prop': 'imageinfo', 'iiprop': 'url'})
                image_json_data = requests.get(new_url).json()

                # image_key = next(iter(image_json_data['query']['pages'].keys()['imageinfo']['url']))
                image_key = next(iter(image_json_data['query']['pages'].keys()))
                url_image = image_json_data['query']['pages'][image_key]['imageinfo'][0]['url']

            # webbrowser.open(url_image, new=new)
                return url_image
        # print(image_json_data)
        except Exception as e:
            details = 'Error fetching image because', e
            print(details)
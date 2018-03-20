from project import flask_setup
from PIL import Image


#(Spotify API) fake audio objects
audio1 = ['Rihanna', 'Rude Boy', 'https://p.scdn.co/mp3-preview/c28012b6e745cf061ff44cbe63cfb03d9cbb5960?cid=d0e072ada0c84e6582fa95e7f7670a36']
audio2 = ['Rihanna', 'Love On The Brain', 'https://p.scdn.co/mp3-preview/104ad0ea32356b9f3b2e95a8610f504c90b0026b?cid=d0e072ada0c84e6582fa95e7f7670a36']
audio3 = ['Rihanna', 'Diamonds', 'https://p.scdn.co/mp3-preview/c28012b6e745cf061ff44cbe63cfb03d9cbb5960?cid=d0e072ada0c84e6582fa95e7f7670a36']
audio_objects = [audio1, audio2, audio3]

#(Wikipedia API) fake artist info
# artist_info = [Image.open('/Users/tylercaldwell/PycharmProjects/flaskhelp/static/rihanna.jpg'), 'Rihanna is a Barbadian Singer, songwriter and actress.']

#(Youtube API) fake artist youtube video
media = "https://www.youtube.com/embed/0RyInjfgNc4"

# This function takes information from the three API calls and displays them using Flask
# audio_objects from the Spotify API, artist_info from the Wikipedia API, youtube_video from the Youtube API]
def display_accept_arugements(audio_objects, artist_info, media):
    # Assuming audio_objects is an collection of objects each with (artist_name, song_title, song_url)
    artist_name = audio_objects[0][0]
    song_titles = []
    song_urls = []
    for object in audio_objects:
        song_titles.append(object[1])
        song_urls.append(object[2])

    # Assuming artist_info is an object with an image(rihanna.jpg), and text("Rihanna is ....")
    artist_image = artist_info[0]
    image_path = '/Users/tylercaldwell/PycharmProjects/flaskhelp/static/%s.jpg' % artist_name
    artist_image.save(image_path)
    image = '/static/%s.jpg' % artist_name
    info = artist_info[1]

    flask_setup.displayprofile(artist_name, image, info, media, song_titles, song_urls)

    flask_setup.runapp(artist_name)


#TODO Replace the following code with data from the api calls
#(Spotify API) fake audio objects
audio1 = ['Rihanna', 'Rude Boy', 'https://p.scdn.co/mp3-preview/c28012b6e745cf061ff44cbe63cfb03d9cbb5960?cid=d0e072ada0c84e6582fa95e7f7670a36']
audio2 = ['Rihanna', 'Love On The Brain', 'https://p.scdn.co/mp3-preview/104ad0ea32356b9f3b2e95a8610f504c90b0026b?cid=d0e072ada0c84e6582fa95e7f7670a36']
audio3 = ['Rihanna', 'Diamonds', 'https://p.scdn.co/mp3-preview/c28012b6e745cf061ff44cbe63cfb03d9cbb5960?cid=d0e072ada0c84e6582fa95e7f7670a36']
audio_objects = [audio1, audio2, audio3]

#(Wikipedia API) fake artist info
# artist_info = [Image.open('/Users/tylercaldwell/PycharmProjects/flaskhelp/static/rihanna.jpg'), 'Rihanna is a Barbadian Singer, songwriter and actress.']
artist_info = []
#(Youtube API) fake artist youtube video
media = "https://www.youtube.com/embed/0RyInjfgNc4"


display_accept_arugements(audio_objects, artist_info, media)

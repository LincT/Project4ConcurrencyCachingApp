from project.CacheHandler import CacheIO
from project.audio import Audio
from project.image_fetcher import image_fetcher
import requests
import webbrowser
import logging
from flask import Flask, render_template, request

cache = CacheIO()
audioApi = Audio()
pic = image_fetcher()

#Configure the logger to write files to tunedin.log
logging.basicConfig(filename='tunedin.log', level=logging.INFO)


def initialize():
    """
    any startup logic goes here
    """
    pass


def display_accept_arugements(audio_objects):
    # Assuming audio_objects is an collection of objects each with (artist_name, song_title, song_url)
    artist_name = str(str(audio_objects[0]).split(",")[0]).split(":")[0]
    song_titles = []
    song_urls = []
    for string in audio_objects:
        song_titles.append(str(string).split(",")[0].split(":")[1].strip())
        song_urls.append(str(string).split(",")[1].strip())

    image = pic.fetch(artist_name)
    info = get_lyrics(artist_name.strip()+":" + str(song_titles[0]).strip())

    return artist_name, image, info, song_titles, song_urls

def get_results(term):
    # query the api's here
    # also query/update the cache
    results = [str(each) for each in cache.search(term=term)]
    if len(results) < 1:  # if no results or an error, check for new data
        new_data = audioApi.search(term)
        results += new_data
        cache.add_record(term, 'spotipy', "^|".join(new_data))
    # print(results)

    # in theory all api's should have returned data by this point,
    # we then return the result data to the calling method
    return results


def get_lyrics(term):
    try:
        if len(str(term).split(":")) > 1:
            artist = str(term).split(":")[0].strip().replace(" ", "%20")
            song_title = str(term).split(":")[1].strip().replace(" ", "%20")
            url = "https://api.lyrics.ovh/v1/{}/{}".format(artist, song_title)
            #print(url)
            lyrics = str(requests.get(url).json()["lyrics"])  # .replace('\n', '<br>')
            return lyrics
        else:
            return "no valid lyrics"
    except KeyError:
        logging.info("ERROR LOADING LYRICS: %s" % url)
        return "Error finding lyrics"

def query_user(prompt):
    # currently just a wrapper
    # needs some form of validation
    # for now min chars = 3 as I imagine spotify would be happy if we weren't
    # spamming them with 1 letter search queries
    user_answer = ""
    while len(user_answer.strip()) < 3:
        user_answer = input(prompt + "\n")
    return user_answer


def generate_view(data_list):
    # place holder for a better display method
    display_list = []
    if len(data_list) > 0:
        for each in data_list:
            if "^|" in str(each):
                for string in str(each).split("^|"):
                    display_list.append(string)
            else:
                display_list.append(each)

        # for each in display_list:
        #     url = str(each)
        #     if len(url.split(",")) == 2:
        #         subUrl = (url.split(",")[1]).strip()
        #         print(url)
        #         if subUrl is None:
        #             print(55, subUrl)
        #             pass
        #         elif subUrl == "None":
        #             print(58, subUrl)
        #             pass
        #         else:
        #             webbrowser.open(subUrl)
        # print(display_list)
        #display_accept_arugements(
        #    display_list,
        #    r"..\tests\Lady_Gaga_Glitter_and_Grease2.jpg",
        #    "https://www.youtube.com/watch?v=Z6hL6fkJ1_k")

        return display_list


def main():

    app = Flask(__name__)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            term = request.form['search']
            if term == '':
                error = 'Empty search. Please enter an artist or song.'
            else:
                logging.info("USER SEARCHED: %s" % term)
                get_lyrics(term)
                results = []
                for each in get_results(term):
                    results.append(each)
                display_list = generate_view(results)

                artist_name, image, info, song_titles, song_urls = display_accept_arugements(display_list)

                return render_template('display.html', artist_name=artist_name, image=image, info=info,
                                       song_titles=song_titles, song_urls=song_urls)

        return render_template('login.html', error=error)

    webbrowser.open('http://127.0.0.1:5000/login')
    app.run()


if __name__ == '__main__':
    main()

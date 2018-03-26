from project.CacheHandler import CacheIO
from project.audio import Audio
from project.bookmarks import BookMarks
from project import flask_setup
from project.image_fetcher import image_fetcher
import requests

cache = CacheIO()
audioApi = Audio()
bookmarks = BookMarks()
pic = image_fetcher()


def initialize():
    """
    any startup logic goes here
    """
    pass


def add_bookmark():
    # saves a staged bookmark, see bookmarks.py for more info
    bookmarks.commit()


def load_bookmark(song_name):
    flask_setup.displayprofile(artist_name, image, info, media, song_titles, song_urls)
    flask_setup.runapp(artist_name)

def display_accept_arugements(audio_objects, artist_info, media):
    # Assuming audio_objects is an collection of objects each with (artist_name, song_title, song_url)
    artist_name = str(str(audio_objects[0]).split(",")[0]).split(":")[0]
    song_titles = []
    song_urls = []
    for string in audio_objects:
        song_titles.append(str(string).split(",")[0].split(":")[1].strip())
        song_urls.append(str(string).split(",")[1].strip())

    # Assuming artist_info is an object with an image(rihanna.jpg), and text("Rihanna is ....")
    artist_image = artist_info[0]
    # artist_image.save(image_path)
    image = pic.fetch(artist_name)
    info = get_lyrics(artist_name.strip()+":" + str(song_titles[0]).strip())

    flask_setup.displayprofile(artist_name, image, info, media, song_titles, song_urls)

    # since we already have the info we can stage the bookmark instead of trying to pull from the html again
    bookmark_dict = {
        "artist_name":artist_name,
        "image": image,
        "text":info,
        "media":media,
        "song_titles":song_titles,
        "song_urls":song_urls
    }
    bookmarks.stage(bookmark_dict)

    flask_setup.runapp(artist_name)


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
    if len(str(term).split(":")) > 1:
        artist = str(term).split(":")[0].strip().replace(" ", "%20")
        song_title = str(term).split(":")[1].strip().replace(" ", "%20")
        url = "https://api.lyrics.ovh/v1/{}/{}".format(artist, song_title)
        lyrics = str(requests.get(url).json()["lyrics"])  # .replace('\n', '<br>')
        return lyrics
    else:
        return "no valid lyrics"


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
        display_accept_arugements(
            display_list,
            r"..\tests\Lady_Gaga_Glitter_and_Grease2.jpg",
            "https://www.youtube.com/watch?v=Z6hL6fkJ1_k")


def main():
    term = query_user("please type the name of a song or artist")
    get_lyrics(term)
    results = []
    for each in get_results(term):
        results.append(each)

    generate_view(results)


if __name__ == '__main__':
    main()

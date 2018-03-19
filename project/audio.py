import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from project.keys import KeyDefinitions


class Audio:

    secrets = KeyDefinitions.keys()

    spotify_id = secrets.get("spotify_id")
    spotify_secret = secrets.get("spotify_secret")
    creds = (SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret))

    def search(self, parms):
        result_set = []
        self.auth()
        try:
            call = spotipy.Spotify(client_credentials_manager=Audio.creds).search(q=parms, limit=3, type='track')
            for each in list(dict(dict(call)["tracks"])["items"]):
                item_dict = dict(each)
                if "preview_url" in item_dict.keys():
                    artist = dict(item_dict["artists"][0])['name']
                    title = item_dict["name"]
                    preview_url = item_dict["preview_url"]
                    item = "{}: {}, {}".format(artist, title, preview_url)
                    result_set.append(item)
            return result_set

        except spotipy.SpotifyException:
            print("Error with spotify credentials")
            return []

    def auth(self):
        if "spotify_id" not in Audio.secrets:
            raise SpotifyCredentialsException

        elif "spotify_secret" not in Audio.secrets:
            raise SpotifyCredentialsException


class SpotifyCredentialsException(Exception):
    __message__ = ""
    def __init__(self):
        self.__message__ = "Please verify credentials present\n"\
        "for more help, see:\n"\
        "https://developer.spotify.com/"
        quit()

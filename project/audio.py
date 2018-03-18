import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from project.keys import KeyDefinitions


class Audio:

    secrets = KeyDefinitions.keys()

    spotify_id = secrets.get("spotify_id")
    spotify_secret = secrets.get("spotify_secret")
    creds = (SpotifyClientCredentials(client_id=spotify_id, client_secret=spotify_secret))

    @staticmethod
    def search(parms):
        call = spotipy.Spotify(client_credentials_manager=Audio.creds).search(q=parms, limit=3, type='track')
        result_set = []
        for each in list(dict(dict(call)["tracks"])["items"]):
            item_dict = dict(each)
            if "preview_url" in item_dict.keys():
                artist = dict(item_dict["artists"][0])['name']
                title = item_dict["name"]
                preview_url = item_dict["preview_url"]
                item = "{}: {}, {}".format(artist, title, preview_url)
                result_set.append(item)
        return "\n".join(result_set)

    def auth(self):
        pass

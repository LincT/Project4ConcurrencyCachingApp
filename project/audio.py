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
        print(parms)
        # print(Audio.spotify.prefix)

        call = spotipy.Spotify(client_credentials_manager=Audio.creds).search(q=parms, limit=3)
        return call

    def auth(self):
        pass

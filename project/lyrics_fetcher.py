import requests


class LyricsFetcher():
    def fetch(self, term):
        if len(str(term).split(":")) > 1:
            artist = str(term).split(":")[0].strip().replace(" ", "%20")
            song_title = str(term).split(":")[1].strip().replace(" ", "%20")
            url = "https://api.lyrics.ovh/v1/{}/{}".format(artist, song_title)
            lyrics = str(requests.get(url).json()["lyrics"])  # .replace('\n', '<br>')
            return lyrics
        else:
            return "no valid lyrics"

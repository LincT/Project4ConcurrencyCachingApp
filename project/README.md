# Capstone Project 4 - APIs, Concurrency and Caching Application
> The application will let the user discover more information on a song or artist of their choice.

To run:
One may wish to use a virtual environment depending on what one already has installed.
One will also need a spotify api key (sorry but those are linked to spotify accounts so best not shared), the other api's should work without keys. copy the body of keys.txt to a new file named keys.py. (git ignore has keys.py as an ignored file for the user's security)
add the following: 

  `details.setdefault("spotify_id", "your_id_here")`
  
  `details.setdefault("spotify_secret", "your_spotify_project_secret_here")`

Requirements are in requirements.txt, `pip install -r requirements` to automatically install.
upon running the app, a new page should load with a search box
One can type in just an artist name to get 3 songs of that artist.
One can also type in just a song to try and find 3 versions of that song.
A third option is if one is relatively certain in the song they want,
one can type in artist: songname to perform a more targeted search.

completed:
fetching images(if available)
fetching lyrics
fetching music from spotify
caching

Partially complete:
bookmarking

Api Name | HomePage
--- | ---
Spotify|https://developer.spotify.com/web-api/
Wikipedia api|https://www.mediawiki.org/wiki/API:Main_page
Lyrics|https://lyricsovh.docs.apiary.io

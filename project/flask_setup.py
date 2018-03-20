import webbrowser
from flask import Flask, render_template


app = Flask(__name__)

# Send the data to the display.html template
def displayprofile(artist_name, image, info, media, song_titles, song_urls):
    @app.route('/')
    @app.route('/<search>')
    def profile(search=None):
        return render_template('display.html', search=search, artist_name=artist_name, image=image, info=info, media=media, song_titles=song_titles, song_urls=song_urls)

# Open the webbrowser and run flask
def runapp(name):
    webbrowser.open('http://127.0.0.1:5000/' + name)
    app.run()


from project import flask_setup


class ViewPortal():
    def display_accept_arugements(self, audio_objects, text, artist_image, artist_name):
        # Assuming audio_objects is an collection of objects each with (artist_name, song_title, song_url)
        print(str(audio_objects))
        song_titles = []
        song_urls = []
        for string in audio_objects:
            song_titles.append(str(string).split(",")[0].split(":")[1].strip())
            song_urls.append(str(string).split(",")[1].strip())

        # flask_setup.displayprofile(artist_name, artist_image, text, artist_image, song_titles, song_urls)
        flask_setup.displayprofile(artist_name,artist_image,text,"",song_titles,song_urls)

        flask_setup.runapp(artist_name)

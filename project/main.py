from project.CacheHandler import CacheIO
from project.audio import Audio
from project.display import ViewPortal
from project.image_fetcher import image_fetcher
from project.lyrics_fetcher import LyricsFetcher

cache = CacheIO()
audioApi = Audio()
pic = image_fetcher()
lyrics = LyricsFetcher()
viewer = ViewPortal()


def initialize():
    """
    any startup logic goes here
    """
    pass


def display_accept_arugements(audio_objects, text, image, artist_name):
    # keeping the wrapper as it used to be a full function
    # TODO remove dependency on this wrapper and wire directly to function
    viewer.display_accept_arugements(audio_objects, text, image, artist_name)


def get_results(term):
    # query the api's here
    # also query/update the cache
    # TODO build results as either text, or links in list/tuple
    music = []
    artist_name = term.split(":")[0].strip().title()
    song_title = term.split(":")[1].strip().title()

    music.append(cache.search_advanced(term=song_title, api="spotipy"))
    print("38 music", music)

    artist_image = cache.search_advanced(term=artist_name, api="image")
    print("41 artist_image", artist_image)

    lyric_text = cache.search_advanced(term=song_title, api="lyrics")

    if len(music) < 1:  # if no results or an error, check for new data
        music = "\n".join(str(each) for each in audioApi.search("{}: {}".format(artist_name, song_title)))
        print(music)
        cache.add_record(song_title, 'spotipy', "^|".join(music))

    if len(artist_image) < 1:
        artist_image = pic.fetch(artist_name)
        print(artist_image)
        cache.add_record(artist_name, 'image', artist_image)

    if len(lyric_text) < 1:
        lyric_text = get_lyrics("{}: {}".format(artist_name, song_title))
        cache.add_record(song_title, "lyrics", lyric_text)

    # in theory all api's should have returned data by this point,
    # we then return the result data to the calling method
    results = {
        "spotipy": music,
        "image": artist_image,
        "lyrics": lyric_text,
        "artist_name": artist_name
    }
    return results


def get_lyrics(term):
    return lyrics.fetch(term.title().strip().replace(" ", "%20"))


def query_user(prompt, format_string=""):
    # for now min chars = 3 as I imagine api's would be happy if we weren't
    # spamming them with 1 letter search queries
    collected_answers = []

    for line in list(prompt):
        user_answer = ""
        while len(user_answer) <= 3:
            user_answer = input("{}:\n".format(line))
            collected_answers.append(user_answer)
    return_string = format_string.join(collected_answers)
    return return_string


def generate_view(music_data_list, artist_image, lyric_text, artist_name):
    # place holder for a better display method
    display_list = []
    print(music_data_list)
    if len(music_data_list) > 0:
        for each in music_data_list:
            if "^|" in str(each):
                for string in str(each).split("^|"):
                    display_list.append(string)
            else:
                print(each)
                for item in each:
                    display_list.append(item)
    display_accept_arugements(display_list, lyric_text, artist_image, artist_name)


def main():
    # cli entry point
    queries = ("Please type the name of an artist", "Please type the name of a song you'd like to search for")
    term = query_user(queries, ": ")
    results = get_results(term)
    print(results)
    music = results["spotipy"]
    image = results["image"]
    artist_name = results["artist_name"]
    lyric_text = results["lyrics"]
    generate_view(music, image, lyric_text, artist_name)


if __name__ == '__main__':
    main()

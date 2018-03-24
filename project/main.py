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


def display_accept_arugements(audio_objects, text, image):
    # keeping the wrapper as it used to be a full function
    # TODO remove dependency on this wrapper and wire directly to function
    viewer.display_accept_arugements(audio_objects, text, image)


def get_results(term):
    # query the api's here
    # also query/update the cache
    # TODO build results as either text, or links in list/tuple
    artist_name = term[0]
    song_title = term[1]
    music = [str(each) for each in cache.search(term=song_title)]
    artist_image = cache.search(term=artist_name)
    lyric_text = cache.search(song_title)

    if len(music) < 1:  # if no results or an error, check for new data
        audio_records = audioApi.search(song_title)

        artist_image = pic.fetch(artist_name)
        lyric_text = get_lyrics(song_title)
        results += audio_records
        cache.add_record(song_title, 'spotipy', "^|".join(audioApi))
        cache.add_record(artist_name,'image', artist_image)
        cache.add_record(song_title,"lyrics",lyric_text)

    # in theory all api's should have returned data by this point,
    # we then return the result data to the calling method
    return results


def get_lyrics(term):
    return lyrics.fetch(term)


def query_user(prompt, format_string=""):
    # for now min chars = 3 as I imagine api's would be happy if we weren't
    # spamming them with 1 letter search queries
    user_answer = ""
    collected_answers = []
    for line in prompt:
        while len(user_answer.strip()) < 3:
            user_answer = input(format_string.format(line))
        collected_answers.append(user_answer)
    return collected_answers


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

        display_accept_arugements(
            display_list,
            r"..\tests\Lady_Gaga_Glitter_and_Grease2.jpg",
            "https://www.youtube.com/watch?v=Z6hL6fkJ1_k")


def main():
    # cli entry point
    queries = ("Please type the name of an artist", "Please type the name of a song you'd like to search for")
    term = query_user(queries, "{}\n")
    results = get_results(term)
    generate_view(results)


if __name__ == '__main__':
    main()

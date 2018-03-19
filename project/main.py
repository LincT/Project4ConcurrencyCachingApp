from project.CacheHandler import CacheIO
from project.audio import Audio
import webbrowser

cache = CacheIO()
audioApi = Audio()

def initialize():
    """
    any startup logic goes here
    """
    pass


def get_results(term):
    # query the api's here
    # also query/update the cache
    results = [str(each) for each in cache.search(term=term)]
    if len(results) < 1:  # if no results or an error, check for new data
        new_data = audioApi.search(term)
        results += new_data
        cache.add_record(term, 'spotipy', "^|".join(new_data))
    print(results)

    # in theory all api's should have returned data by this point,
    # we then return the result data to the calling method
    return results


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

        for each in display_list:
            url = str(each)
            if len(url.split(",")) == 2:
                subUrl = (url.split(",")[1]).strip()
                print(url)
                if subUrl is None:
                    print(55, subUrl)
                    pass
                elif subUrl == "None":
                    print(58, subUrl)
                    pass
                else:
                    webbrowser.open(subUrl)

        return "your results should open momentarily in a new window"
    else:
        return "no data to display"


def main():
    term = query_user("please type the name of a song or artist")

    results = []
    for each in get_results(term):
        results.append(each)

    print(generate_view(results))


if __name__ == '__main__':
    main()

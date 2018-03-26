from project.sql_handler import DataBaseIO
import datetime


class BookMarks():
    # for now having the bookmarks live in the same db as the cache
    # should db size become an issue, then it might be better to split the db
    __bookmarkDB__ = DataBaseIO('cache_database')
    __bookmark_table_name__ = "bookmarks"
    staged_bookmark = dict()

    def __init__(self):
        self.__bookmarkDB__.create_table("bookmarks",
                                'entry_id integer PRIMARY KEY, '
                                'datetime text NOT NULL, '
                                'entry_name text NOT NULL, '
                                'image_url text NOT NULL, '
                                'lyrics_text text NOT NULL,'
                                'music_url text NOT NULL')

    def __str__(self):
        db = self.__bookmarkDB__
        tables = [str(each) for each in db.spew_tables()]
        verbose_table_data = ""
        for each in tables:
            fields = ", ".join(item for item in db.spew_header(each))
            contents = "\n".join("\t\t" + str(item) for item in db.execute_query(each))
            verbose_table_data += str("table: " + each + "\n\tfields: " + fields + "\n\tcontents:\n" + contents)

        return verbose_table_data

    def add(self, name, image_url, lyrics_text, music_url):
        db = self.__bookmarkDB__
        table = self.__bookmark_table_name__
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        data = ", ".join([now, name, image_url, lyrics_text, music_url])
        column_list = "datetime,entry_name,image_url,lyrics_text,music_url"
        db.add_record(table, column_list, data)

    def remove(self,bookmark_name):
        db = self.__bookmarkDB__
        table = self.__bookmark_table_name__
        db.delete_record(table,"entry_name", bookmark_name)

    def query(self, term):
        db = self.__bookmarkDB__
        table = self.__bookmark_table_name__
        results = "\n".join([str(each) for each in db.execute_query(table, parm=term)])
        return results

    def list(self):
        db = self.__bookmarkDB__
        table = self.__bookmark_table_name__
        results = "\n".join([str(each) for each in db.execute_query(table, "entry_name")])
        return results

    def stage(self, bookmark_dict):

        self.staged_bookmark = bookmark_dict

    def commit(self):
        # save a pre-staged bookmark
        # future development will try and intuit data from what is sent instead of the man
        bm = dict(self.staged_bookmark)
        bookmark_name = "{}: {}".format(bm.get("artist_name"),bm.get("song_titles")[0])
        image = bm.get("image")
        lyrics = bm.get("text")
        music = bm.get("song_urls")

        self.add(name=bookmark_name, image_url=image, lyrics_text=lyrics, music_url=music)

from project.sql_handler import DataBaseIO as dbio
import datetime


class CacheIO:

    """
    this class should record the search term, get the date and time, and record the json to the sql handler
    logic regarding how long to keep an object cached should operate here based on parameters passed into the class
    this class should return an existing archive, or return "" if no previous entry exists based on sql search
    """
    DBCache = dbio('cache_database')
    table_name = 'api_json_return_values'
    result_ttl = 300  # time in seconds for results to be kept

    def __init__(self, result_ttl=300):
        """
        create a class instance with a constant time to live, if none specified, then default
        :param result_ttl: int
        """
        self.result_ttl = result_ttl
        self.__initialize_cache__()

    def __str__(self):
        """
        might refactor this to live in sql_handler
        :return:
        """
        tables = [str(each) for each in self.DBCache.spew_tables()]
        verbose_table_data = ""
        for each in tables:
            fields = ", ".join(item for item in self.DBCache.spew_header(each))
            contents = "\n".join("\t\t" + str(item) for item in self.DBCache.execute_query(each))
            verbose_table_data += str("table: " + each + "\n\tfields: " + fields + "\n\tcontents:\n" + contents)

        return verbose_table_data

    def search(self, term):
        """
        check database for records within lifecycle
        return relevant result
        if no result, return a standard message to indicate such
        """
        db = self.DBCache
        results = db.execute_query(table='api_json_return_values', regex=term)
        if len(results) > 0:
            return results
        else:
            return []

    def add_record(self, term):
        current_datetime = self.get_date_time()
        api = 'test_api'
        query_term = term
        json = '{some_test_json:some_test_result}'
        field_data = "'{}', '{}', '{}', '{}'".format(current_datetime, api, query_term, json)
        print(field_data)
        self.DBCache.add_record('api_json_return_values',
                                'datetime, api_name, query_term, api_result_text',
                                field_data)


    @staticmethod
    def get_date_time():
        # https://stackoverflow.com/a/7999977
        # truncating off milliseconds
        # returning utc for consistency regardless of locale or daylight savings rules
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    def __initialize_cache__(self):
        self.DBCache.drop_table(self.table_name)
        self.DBCache.create_table(self.table_name,
                                  'result_id integer PRIMARY KEY, '
                                  'datetime text NOT NULL, '
                                  'api_name text NOT NULL, '
                                  'query_term text NOT NULL, '
                                  'api_result_text text NOT NULL')
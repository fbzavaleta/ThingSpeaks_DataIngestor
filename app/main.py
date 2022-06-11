"""
--Data ingestor engine for thingspeak API
--Please read the README of the project to 
--set your enviroment
@autor: Eng. Francis Zavaleta
"""
from ast import If
from dotenv import load_dotenv
import objects.DataUtils as du
import objects.DatabaseUtils as db
import os
import requests

load_dotenv()


class ingestor_engine:
    def __init__(self) -> None:
        pass

    def main(self):
        self.__build_databases_tables()
        destinity_table = self.__get_parameters("SQL_MAIN_TABLE")
        data_to_insert = self.generate_dataframe()
        len_of_data = data_to_insert.shape[0]
        print("[engine] Searching new data to insert in database . . .")
        if self.__ingest_discriminator(data_to_insert, destinity_table) == "ok":
            print("[engine] inserting rows in database . . .")
            for row in range(0, len_of_data):
                values = data_to_insert.iloc[row].to_dict()
                try:
                    db.database().ingest(
                        values=values,
                        query_str=self.__build_insert_query(values, destinity_table),
                    )
                except:
                    print("[engine] got error on {} row".format(row))
        else:
            print("[engine] Nothing to fetch")
        print("[engine] All done, we are finished")

    def generate_dataframe(self):
        get_data_from_channel = requests.get(self.__build_url()).json()
        all_data_feed = get_data_from_channel["feeds"]

        sensor = du.operators(
            col=self.__get_parameters("ROW_FEED_FIELDS").split("+"),
            json_data=all_data_feed,
        )
        sensor_df = sensor.gen_dataframe()

        return sensor.clean_data(
            sensor_df, new_col=self.__get_parameters("ROW_DATABASE_FIELDS").split("+")
        )

    def __build_url(self):
        base_url = "{base}{channel}/feed.json?results={nrows}"
        return base_url.format(
            base=self.__get_parameters("THING_SPEAKS_URL"),
            channel=self.__get_parameters("THING_SPEAKS_CHANNEL_ID"),
            nrows=self.__get_parameters("THING_SPEAKS_ROWS"),
        )

    def __ingest_discriminator(self, df_, table):
        last_id_entry = df_["entry_id"].max()
        query_last_row = db.database().execute_from_str(
            "select max(entry_id) from {};".format(table)
        )
        if query_last_row[0][0] == None:
            query_last_row = [[0]]
        return "ok" if last_id_entry > query_last_row[0][0] else "no"

    def __get_parameters(self, parameter):
        return os.environ.get(parameter)

    def __build_databases_tables(self):
        data_engine = db.database()
        try:
            data_engine.execute_from_query(
                sql_file=self.__get_parameters("FILE_SQL_NAME")
            )
        except:
            print("[engine] Database tables already exist!!!")

    def __build_insert_query(self, dict_data, table):
        insert_str = "insert into {table} {fields} values {values};"
        fields = "{}".format(tuple(dict_data.keys()))
        values = "{}".format(tuple(dict_data.values()))

        return insert_str.format(table=table, fields=fields, values=values).replace(
            "'", ""
        )


ingestor_engine().main()

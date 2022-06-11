import mysql.connector
import os

from pandas import DataFrame

par_db = {
    "host": "db",
    "database": "data_sensors",
    "user": "root",
    "password": "root",
}

class database:
    def __init__(self):
        self.dir = os.getcwd()
        self.cnx_mysql = mysql.connector.connect(
            host=par_db.get("host"),
            user=par_db.get("user"),
            database=par_db.get("database"),
            password=par_db.get("password"),
        )
        

    def execute_from_query(self, sql_file):
        with open(self.dir + "/" + sql_file, "r") as reads:
            sqlScript = reads.read()
            cursor_cnxn_msql = self.cnx_mysql.cursor()
            cursor_cnxn_msql.execute(sqlScript)

    def ingest(self, values:dict, query_str):
        insert_query = query_str.format(**values)

        cursor_cnxn_msql = self.cnx_mysql.cursor()
        cursor_cnxn_msql.execute(insert_query)
        self.cnx_mysql.commit()
    
    def execute_from_str(self, str_sql):
        cursor_cnxn_msql = self.cnx_mysql.cursor()
        cursor_cnxn_msql.execute(str_sql)
        data_rows = cursor_cnxn_msql.fetchall()

        return data_rows

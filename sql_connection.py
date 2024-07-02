import pymssql
from langchain_community.utilities.sql_database import SQLDatabase
import os

server = os.getenv("IP")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE_NAME")

connection_string = f'mssql+pymssql://{username}:{password}@{server}/{database}'


mssql_conn = pymssql.connect(server, username, password, database)
mssql_cursor = mssql_conn.cursor(as_dict=True)


def return_database(connection_string):
    db = SQLDatabase.from_uri(connection_string)
    return db

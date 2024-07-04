import pymssql
from langchain_community.utilities.sql_database import SQLDatabase
import os

SERVER:str = os.getenv("IP")
USERNAME: str = os.getenv("USERNAME")
PASSWORD: str = os.getenv("PASSWORD")
DATABASE: str = os.getenv("DATABASE_NAME")
ENCODED_PASSWORD: str = os.getenv("ENCODED_PASSWORD")


connection_string = f'mssql+pymssql://{USERNAME}:{ENCODED_PASSWORD}@{SERVER}/{DATABASE}'

mssql_conn = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)

mssql_cursor = mssql_conn.cursor(as_dict=True)


def return_database(connection_string) -> SQLDatabase:
    db = SQLDatabase.from_uri(connection_string)
    return db
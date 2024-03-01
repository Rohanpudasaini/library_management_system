import os
from sqlalchemy import text, create_engine, URL, inspect
from sqlalchemy.orm import Session

from dotenv import load_dotenv
from databse_connection.models import create_database
from cli_components import error_assci

load_dotenv()

host = os.getenv('host')
database = os.getenv('database')
user = os.getenv('user')
password = os.getenv('password')


url = URL.create(
    database=database,
    username=user,
    password=password,
    host=host,
    drivername="postgresql"
)
engine = create_engine(url)
session = Session(bind=engine)
tables = inspect(engine).get_table_names()

if len(tables) < 9:
    error_assci()
    print("Incomplete Database found, Deleting the database to create a new one from scratch")
    print("Do you want to continue??(Y/N)")
    user_in = input("\n\t:").strip().lower()
    if user_in == 'n':
        exit()
    dummy_data = False
    dummy = input("Do you want a dummy data on databse?(y/n)").strip().lower()
    if dummy == 'y':
        dummy_data = True
    if tables:
        table_string = ", ".join(tables)
        session.execute(text(f"DROP TABLE {table_string};"))
    create_database(engine,  dummy_data, session,)
    print("Database Created")

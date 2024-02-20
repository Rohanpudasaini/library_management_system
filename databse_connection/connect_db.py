import os
from sqlalchemy import text, create_engine, URL, inspect
from sqlalchemy.orm import Session
# from sqlalchemy.ext.automap import automap_base
from dotenv import load_dotenv
from databse_connection.create_table_schema import create_database, Librarian, Magazine, MemberBooks, User, Books,\
    Publisher, Record, MemberMagazine
# import create_table , 
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
engine = create_engine(url,echo=False)
session = Session(bind=engine)
# print(engine.table_names())
tables = inspect(engine).get_table_names()
print(len(tables))
if len(tables) < 9:
    print("Incomplete Database found, Deleting the database \
        to create a new one from scratch \n\
            \n------------------------------\
                Do you want to continue??(Y/N)")
    user_in = input("\t:").lower()
    if user_in == 'n': exit()
    dummy_data = False
    dummy = input("Do you want a dummy data on databse?(y/n)").lower()
    if dummy == 'y': dummy_data = True
    if tables:
        table_string = ", ".join(tables)
        session.execute(text(f"DROP TABLE {table_string};"))
    create_database(engine,session, dummy_data)
    print("Database Created")
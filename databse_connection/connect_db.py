import os
from sqlalchemy import create_engine, URL, inspect
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from dotenv import load_dotenv
# import create_table
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

# if (inspect(engine).has_table('users')):
#     create_table.create_user()
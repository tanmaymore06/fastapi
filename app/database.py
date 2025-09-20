# In this file, 1) we are going to establish a connection to a PostgreSQl database using the DATABSE_URL which is in the env. file,
#               2) build a session using the session_maker() which'll help to execute SQL commands, and
#               3) Declare the Base class using the declarative_base(). The Base class provides functionalities to make a Python class as an ORM Model.

from sqlalchemy import create_engine # The engine sets the connection to the database
from sqlalchemy.orm import sessionmaker, declarative_base
import os 
from dotenv import load_dotenv

load_dotenv() # Load the content of the env. file
DATABASE_URL = os.getenv("DATABASE_URL") # Store the database info in a variable to use it while creating an engine

engine = create_engine(DATABASE_URL) # Connects to the database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Whenever we need to execute some SQL commands, we've to make an instance of the SessionLocal
# The autocommit=False means that changes to the database won't be committed automatically, and autoflush=False means that changes won't be flushed to the database automatically
# The bind=engine binds the SessionLocal to the engine 

Base = declarative_base()

def get_db(): # Dependency function to get a database session. This function will be used with the Depends function to provide a database session to path operation functions.
    db = SessionLocal() # Session object is what resposnsible for talking to the database. Using the db object, we can perform various database operations like querying, inserting, updating, and deleting records.
    try:
        yield db # Yielding the db session allows FastAPI to manage the session's lifecycle. It will create a new session for each request and close it after the request is completed.
    finally:
        db.close() # Closing the db session to release database connections and resources.


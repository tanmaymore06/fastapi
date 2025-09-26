# In this file, we are going to establish a connection to a PostgreSQl database using the DATABSE_URL which is in the env. file.

from sqlalchemy import create_engine # The engine sets the connection to the database
import os 
from dotenv import load_dotenv

load_dotenv() # Load the content of the env. file
DATABASE_URL = os.getenv("DATABASE_URL") # Store the database info in a variable to use it while creating an engine

engine = create_engine(DATABASE_URL) # Connects to the database

# Now we are ready to make an ORM Model
# In this file, we'll:
#           declare the Base class using the declarative_base(). The Base class provides functionalities to make a Python class as an ORM Model.
# The ORM Model is actually a schema that defines the structure of a database table if and only if it doesn't exist already. If the table name already exists, it won't create a new table.
# Each class variable represents a column in the table, and the class itself represents the table structure. 

from sqlalchemy.orm import declarative_base,base
from sqlalchemy import Column, Integer, Boolean, String

base = declarative_base() # Base class to create ORM Models. Any class that inherits from this base class will be an ORM Model

class Post(base):
  __tablename___ = 'posts'

  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, default=True) # 'default=True' is not a right way to set a default value in the database. 
  # We have to use 'server_default=True' to set a default value in the database which will be corrected in the next commit.
  # The difference between 'default=True' and 'server_default=True' is that the former sets a default value at the application level, while the latter sets it at the database level.

# The "model.base.metadata.create_all(dind=engine)" in the main.py file will look for a database table named 'posts' in the database and if it doesn't find one, it will create the table using the structure defined in this ORM Model.
# Let's say we want to change a specification of a column or add a new column to the table, we can simply modify this ORM Model and run the application again but because the table name already exists in the database, it won't make any changes to the existing table.


# The drawback of using ORM Models is that if we make any changes to the model, it won't reflect in the database automatically.
# To make changes in the database schema, we have to use migration tools like Alembic which will be covered in the next commit.

  

# In this file, we'll create a Python class using the Base class to make it an ORM Model. The ORM Model is a model which maps to an existing table in the database
# Each class variable represents a column in the table, and the class itself represents the table structure.

from sqlalchemy.orm import base
from sqlalchemy import Column, Integer, Boolean, String

class Post(base):
  __tablename___ = 'posts'

  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, default=True)

  



from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

Base = declarative_base() # The first letter of the Base should be capitalized

class Post(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, server_default=text('True')) 
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
  # created_at uses the TIMESTAMP type from sqlalchemy and sets the default value to the current time using the text function
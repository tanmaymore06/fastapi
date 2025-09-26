# SQLAlchemy engine with an ORM Model/version2-orm

This commit is the follow-up from the commit **'Version 1: CRUD operations with Raw SQL (with a README)'** of the main branch. This commit introduces on how to use an ORM Model to overcome the SQL injection drawback of the Version 1.

---
## Features 
  - Connects directly to a PostgreSQL database

  - Create new posts
   
  - Read all posts **or** read a single post by ID

  - Update an existing post by 

  - Delete a single post by ID

---

## Tech Stack
  - [FastAPI](https://fastapi.tiangolo.com/) - API Framework

  - [PostgreSQL](https://www.postgresql.org/) - Database

  - [psycopgy2](https://pypi.org/project/psycopg2/) - A database driver for raw SQL queries

  - [pydantic](https://docs.pydantic.dev/latest/) - Used for Data Validation

  - **Added** - [SQLAlchemy](https://docs.sqlalchemy.org/en/20/intro.html#installation) - Used for to securely connect to a database and securely perform SQL operations 

---

## Pre-Commit State: 

  - Manually creating a database, a table with columns and manually creating some 2 or 3 records in it for testing purposes.

  - Creating an instance of the ***FastAPI*** and creating a Pydantic Model which is just a Python class using the ***Pydantic.BaseModel*** to have a schema for whatever JSON info the user provides in order to ***CREATE*** or ***UPDATE*** some records.

  - Using the psycopgy2, we connect with the database and create an object as 'cursor' using the ***conn.cursor()*** which helps us to execute ***raw SQL queries*** using the function ***execute()***.

  - Creating ***Path Operations*** for CRUD operations. A path operation is a combination of a decorator with a function right beneath it. The decorator tells the FastAPI when to execute the function which sits right beneath it. In the parameter we can use, the endpoint's value or the request Body which has the Pydantic schema (the schema we created in the 2nd step).

    ### Drawback:

      - As there are raw sql queries in the the path operations, an attacker may change those queries to whatever they want to fetch or manipulate important records in the database. This kind of attack is called as ***SQL Injections***. 
  
##  How the Code Works Now

  First of all we've to understand what is the ORM and how can it be used to overcome the risk of SQL injections.

  ***What is the ORM (Object Relational Mapping) ?*** It helps us to make tables and it's specifications (i.e., Database Schema) and let us perform any SQL commands we want without writing any SQL commands in the application code. Well in this commit, **I only focused on to create a database schema with the ORM Model**.  

  ***How to use the ORM to Avoid Raw SQL queries ?*** 

  - Step 1: Connect SQLAlchemy with your desired Postgres DB using `create_engine(Database_URL)`. The Database_URL is in the .env file, load it in the application code using `load_dotenv()` and get it using `os.getenv()`. Ofcourse you need to import create_engine from sqlalchemy, os and, from dotenv import load-dotenv.

    ```python
    from sqlalchemy import create_engine
    import os
    from dotenv import load_dotenv

    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    ```

  -  Step 2: Now we've built the connection and its time to make an ORM Model. We need to use a class called as the ***base*** which provides functionalities to make the ORM. But first we need to declare it using `declarative_base()`

      ```python
      from sqlalchemy.orm import declarative_base, base
      from sqlalchemy import Column, Integer, Boolean, String

      base = declarative_base()
      ```
      and then make a child class of the base (***This is the ORM***). This child class is actually a schema of a table we want to create in the DB. In the ORM we just created, we've to specify the table name using `__tablename__=''` and make class variables which are schemas for columns. 

      ```python
      class Post(base):
      __tablename___ = 'posts'

      id = Column(Integer, primary_key=True, nullable=False)
      title = Column(String, nullable=False)
      content = Column(String, nullable=False)
      published = Column(Boolean, default=True)
      ```

  - Step 3: We have a connection to DB in the database.py and the ORM Model in the models.py. But how to let the ORM Model to know the connection we made, so that the ORM will map to the correct DB ? Observe the below code which is in the fastapi app i.e., in the main.py: 
    ```python
    models.base.meatadata.create_all(bind=engine)
    ```
    The above code:
      -  goes to the models.py then,
      - picks the metadata of the class created from the base class ***i.e., picks the specifications of the ORM Model*** then, finally
      - `create_all(bind=engine)` gets the database schema provided by the ORM Model and targets to the connection made by the engine.

## The Drawback and the Next Possible Actions

  - #### The Drawback: 
    Let's say we run the application and the 'posts' table in the desired DB gets created with expected table specifications. There will definitely come a time when we need to change some specification of the 'posts' table e.g., we may need to add an extra column then, will the ORM change the table schema in the DB ?  The answer is ***NO***. The ORM Model we created, is only useful if we dont already have any DB schema.

      - See, i'm treating DB schema and table schema equally because, right now the ORM Model only has one table schema.   

    The process of changing database schema is called as ***SQL Migrations***. That is, the ORM does not support SQL migrations and that's why we need to use a migration tool, the Alembic.

  - #### What we did and Next Steps:

    We :
      - connected SQLAlchemy to the 'fastapi' database,
      - made the ORM Model for the table 'posts', and
      - directed the ORM Model to the connection and created the table schema for the 'posts'.

    Next Steps:
      - we don't know how to query to the database, and
      - don't know how to do SQL Migrations 



    
      
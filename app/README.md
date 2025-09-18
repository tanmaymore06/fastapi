# Learning FastAPI: Version 1 (CRUD Operations with Raw SQL)

A simple backend API built with **FastAPI** and **PostgreSQL**.
This version of the project demonstrates how to directly connect with a database, and how to perform CRUD operations by executing **raw SQL queries**.

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

---

## Getting Started

  ### Pre-requisites
    - Python 3.13.1
    - PostgreSQL installed and running

  ### Setup
    1.  Clone the repositery:
        ```bash
        git clone https://github.com/tanmaymore06/fastapi.git
        cd fastapi```
    2. Install dependencies:
        pip install -r requirements.txt
    3. Start the server:
        uvicorn main:app --reload

---

## The Internal Workings of This Version 1

  - Manually creating a database, a table with columns and manually creating some 2 or 3 records in it for testing purposes.

  - Creating an instance of the ***FastAPI*** and creating a Pydantic Model which is just a Python class using the ***Pydantic.BaseModel*** to have a schema for whatever JSON info the user provides in order to ***CREATE*** or ***UPDATE*** some records.

  - Using the psycopgy2, we connect with the database and create an object as 'cursor' using the ***conn.cursor()*** which helps us to execute ***raw SQL queries*** using the function ***execute()***.

  - Creating ***Path Operations*** for CRUD operations. A path operation is a combination of a decorator with a function right beneath it. The decorator tells the FastAPI when to execute the function which sits right beneath it. In the parameter we can use, the endpoint's value or the request Body which has the Pydantic schema (the schema we created in the 2nd step).

    ### Drawback:

      - As there are raw sql queries in the the path operations, an attacker may change those queries to whatever they want to fetch or manipulate important records in the database. This kind of attack is called as ***SQL Injections***. 

    
      
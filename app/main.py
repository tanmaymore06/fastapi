from fastapi import FastAPI, status,  HTTPException # FastAPI is the main class for creating the API application. status is used to define HTTP status codes. HTTPException is used to raise HTTP exceptions in the API. Depends is used for dependency injection, allowing us to declare dependencies for path operation functions.
from pydantic import BaseModel # BaseModel is used to create data models with validation.
from typing import Optional # Optional is used to indicate that a field is optional (i.e., it may or may not be provided).
import psycopg2  
from psycopg2.extras import RealDictCursor # RealDictCursor is a cursor that returns rows as dictionaries, making it easier to work with the data.
import time
import os 
from dotenv import load_dotenv

# Load an environment variable which has actual database url and is in the '.env' file. 
load_dotenv()

app = FastAPI()  # Create a FastAPI instance to use the functionalities of the FastAPI() class.

# Pydantic model to define the schema of whatever information provided to the server. This ensures us that the user only provides info, we want.
# There can be many reasons to use the below Pydantic model, e.g., to give info to the server so that it can Create or Update data in a database. 
class Post(BaseModel):  
    title: str
    content: str
    published: bool = True # If the user does not provide the key "published", it's value will default to True. That is, published is true whether the user provides it or not.
    rating: Optional[int] = None # rating is optional, so the user may or may not provide it. If not provided, its value will be None.


# Connect to the database
DATABASE_URL = os.getenv("DATABASE_URL") # Get the database url from the .env file 

while True: # To keep trying to connect to the database until a successful connection is made.
    try:
        conn=psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor=conn.cursor() # conn.cursor() gives us a very important function 'execute()' which let's us execute any SQL commands on the database.
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

# Below are all the Path Operations 

@app.get("/")   #By visiting the full address (i.e., wherever the server is running) (Obviously, after starting the server), your browser automatically sends a GET request to the / endpoint(endpoint means last thing of the full address).
                #The decorator @app.get("/") tells FastAPI to detect GET requests to /, execute the root function, and send its response back to the client (your browser).
def root():
    return {"message": "Welcome to my api, hehefff"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

# By visiting the url, you are automatically sending GET request to the url but, to send other HTTP requests to the url we need to use the Postman.
# The Postman enables us to choose any HTTP request by providing the url and also lets us put a request Body (i.e., some info in form of JSON), 
# if we need to. There is a 'Send' button which sends selected HTTP request with the request Body to the provided url.
# The url accepts request Body if and only if it's schema is as same as that of the created Pydantic Model i.e., the Post class.

@app.post("/posts", status_code=status.HTTP_201_CREATED) # 201 status code indicates that a new resource has been successfully created on the server.
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (int(id),))
    p = cursor.fetchone()
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"post_detail": p}
        

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) # 204 status code indicates that the request was successful, but there is no content to send in the response.
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (int(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"message": "post was successfully deleted", "data": delete_post}



@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, int(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return {"updated_data": updated_post}
from fastapi import FastAPI, status,  HTTPException

from pydantic import BaseModel 
from typing import Optional 


from .database import engine
from . import models

models.base.metadata.create_all(bind=engine)
# "models.base.metadata" goes to the the models.py specifically, the ORM Model 'Post(Base)' and gets all the metadata like, table structure, column specifications, etc.,.
# The create_all() creates whatever info present in the ORM Model and targets to the connection to the database created in the engine 



app = FastAPI() 


class Post(BaseModel):  
    title: str
    content: str
    published: bool = True 
    rating: Optional[int] = None 


@app.get("/")   
               
def root():
    return {"message": "Welcome to my api, hehefff"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
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
        

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) 
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
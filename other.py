from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# postgre pass ----- test
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database = 'fastapi', user = 'postgres', password = 'test', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successfull !!!')
        break
    except Exception as error:
        print('Connecting to DB failed')
        print('Error : ', error)
        time.sleep(2)

# my_posts = [
#     {'id': 1,
#     'title': 'top beaches in florida',
#     'content': "check out these awesome beaches"
#     },
#     {
#     'id' : 2,
#     'title' : 'top beaches in florida',
#     'content' : "check out these awesome beaches"
#     }
# ]

def find_id(id):
    for i in my_posts:
        if i['id'] == id:
            return i

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
# def x():
#     pass

# def y():
#     pass

# def amex():
#     pass

# @app.get("/generate")
# def gen_cc(t_cc):
#     if t_cc == visa:
#         number  = x()
#     elif t_cc == mc:
#         number = y()
#     elif t_cc == amex:
#         number = amex()    
#     return number

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                  (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY ID DESC LIMIT 1""")
    last_post = cursor.fetchone()
    return {"details": last_post}

@app.get("/posts/{id}")
def get_post(id: int):                                                  # Need INT so THE URL CAN UNDERSTAND
    cursor.execute("""SELECT * FROM  posts WHERE id = %s""", (str(id),)) # NEED STR for SQL query
    one_post = cursor.fetchone()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: ({id}) wasn't found")
    return {"post_detail": one_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    del_post = cursor.fetchone()
    conn.commit()
    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Such id: {id} not present")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                  (post.title, post.content, post.published, str(id)))
    upt_post = cursor.fetchone()
    conn.commit()
    if upt_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Such id: {id} not present")

    return {'message': upt_post}
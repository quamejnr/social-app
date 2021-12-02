from database import Database
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from starlette.responses import Response


# Initialize app
app = FastAPI()


# Initialize database
database = Database()
conn = database.connect()
cursor = conn.cursor()


# Models
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


# Views
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
                    (post.title, post.content, post.published))
    
    created_post = cursor.fetchone()

    # Save to database
    conn.commit()

    return created_post


@app.get("/posts/drafts")
def get_drafts():
    cursor.execute("SELECT * FROM posts WHERE published = False")
    drafts = cursor.fetchall()
    return drafts


@app.get("/posts/{id}")
def get_post_detail(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", str(id))
    post = cursor.fetchone()
    if post:
        return post
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} not found.")


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", str(id))
    post = cursor.fetchone()
    if post:
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} not found.") 


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
        cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                        (post.title, post.content, post.published, str(id)))
        updated_post = cursor.fetchone()
        if updated_post:
            conn.commit()
            return updated_post      
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {id} not found.")
from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from starlette.responses import Response


# Initializing app
app = FastAPI()


# Models
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {'id': 1, 'title':'Post 1', 'content': 'This is my first post', 'published': True},
    {'id': 2, 'title':'Post 2', 'content': 'This is my second post', 'published': False}
    
]

# helper functions
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_post_index(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index


# Views
@app.get("/posts")
def get_posts():
    return my_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = post.dict()
    id = len(my_posts) + 1
    post['id'] = id
    my_posts.append(post)
    return post


@app.get("/posts/drafts")
def get_drafts():
    drafts = [post for post in my_posts if post['published'] == False]
    return drafts


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts) - 1]
    return latest_post


@app.get("/posts/{id}")
def get_post_detail(id: int):
    post = find_post(id)
    if post:
        return post
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail="Not found.")


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail=f"Not found.") 


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    post = post.dict()
    index = find_post_index(id)
    if index:
        # set updated post id to the id passed in the request
        post['id'] = id
        # replace the existent post with the updated post
        my_posts[index] = post
        return post     
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                        detail=f"Not found.")
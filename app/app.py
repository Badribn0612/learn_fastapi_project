from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse
app = FastAPI()

# @app.get('/hello-world')
# def hello_world():
#     return {"message": "Hello World"}
# # We are mostly going to return a pydantic object or a python dictionary



text_posts = {
    1: {
        "title": "New Post",
        "content": "Cool test post"
    },
    2: {
        "title": "Getting Started with AI",
        "content": "A beginner-friendly guide to understanding how AI works and where to start learning."
    },
    3: {
        "title": "Why RAG Matters",
        "content": "Retrieval-Augmented Generation helps LLMs stay factual by grounding responses in external knowledge."
    }
}

# Reason why you should specify the data type of the arguments is that it can be documented by fastapi
@app.get('/posts')
def get_all_posts(limit: int = None) -> list[PostResponse]:
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get(f'/posts/{id}')
def get_posts(id: int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

# FastAPI automatically validates the data that comes into the API
@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[len(text_posts) + 1] = new_post
    return new_post
# PostResponse is basically a data type that this endpoint will return
# This also improves the documentation
# At the same time handles type checking - so that the output is of the type that we specify

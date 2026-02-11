from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# As far as I understand - what Depends does is basically it will execute the get_async_session and return the db - so that we can use that db into out function
@app.post('/upload')
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
    ):
    post = Post(
        caption = caption,
        url = "dummy url",
        file_type="photo",
        file_name="dummy name"
    )
    session.add(post) # this is basically like staging the changes
    await session.commit() # commit will fully commit the post into the database
    await session.refresh(post) # this will basically go into the database and get us the post that is present in the database
    # for example id and created_at is only present when session.commit - but the post object present here does not have the same
    # to inorder to sync two objects ie between post that is present here and the post that is present in the database - we will do refresh
    return post

# Now inorder to view if the post has been persisted in the database we would have to create a get endpoint
@app.get('/feed')
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption, 
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": posts_data}
# we are going to use Sqlalchemy as our orm
# It basically abstracts sql code in python

from collections.abc import AsyncGenerator
from datetime import datetime
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, null
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, relationship

DATABASE_URL = "sqlite+aiosqlite:///./test.db" # aiosqlite is basically the asynchronous version of sqlite - we can later connect to the production database

# Data model is basically the type of data that we would want to store
# we are going to create a data model to store a post

# We basically cannot inherit from DeclarativeBase directly - hence we would have to inherit in to Base and use that Base going forward
class Base(DeclarativeBase):
    pass

class Post(Base): # inheriting from DeclarativeBase will let fastapi know that we are going to create a data model
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# for now we are going to create the datamodel here - if we have many data model - we will create a file maintain them there and then import those here. 
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

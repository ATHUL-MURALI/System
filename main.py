from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional, List
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
import os


# Load environment variables
load_dotenv()


# Database model
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: bool = False


# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)


# Create tables
def create_all_tables():
    SQLModel.metadata.create_all(engine)


# Lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_all_tables()
    yield


# FastAPI app
app = FastAPI(lifespan=lifespan)


# Create item
@app.post("/items/")
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


# Read all items
@app.get("/items/", response_model=List[Item])
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items
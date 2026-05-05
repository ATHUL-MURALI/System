from sqlmodel import SQLModel, Field
from typing import Optional
from dotenv import load_dotenv
import os

class Item(SQLModel, table=True):
    id : Optional[int] = Field(default = None, primary_key = True)
    name : str
    price : float
    is_offer : bool = False

from sqlmodel import create_engine , Session

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

from fastapi import FastAPI

from contextlib import asynccontextmanager

def create_all_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
def lifespan():
    create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)

@app.post("/items/")
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    
from typing import List
from sqlmodel import select

@app.get("/items/", response_model=List[Item])
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

































































    # import psycopg2
    # from dotenv import load_dotenv
    # import os

    # # Load environment variables from .env
    # load_dotenv()

    # # Fetch variables
    # DATABASE_URL = os.getenv("DATABASE_URL")

    # # Connect to the database
    # connection = psycopg2.connect(DATABASE_URL)

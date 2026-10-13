from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

books = [
    {"id": 1, "title": "Хоббит", "author": "Джон Толкин"},
    {"id": 2, "title": "Маленький принц", "author": "Антуан де Сент-Экзюпери"},
]
next_id = 3


class BookCreate(BaseModel):
    title: str
    author: str


@app.get("/")
def hello():
    return {"message": "Привет, Books App!"}


@app.get("/books")
def get_books():
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book


@app.post("/books", status_code=201)
def create_book(data: BookCreate):
    global next_id
    book = {"id": next_id, **data.model_dump()}
    next_id += 1
    books.append(book)
    return book

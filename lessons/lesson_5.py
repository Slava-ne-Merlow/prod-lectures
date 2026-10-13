from fastapi import FastAPI, HTTPException
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


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None


def find_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")


@app.get("/")
def hello():
    return {"message": "Привет, Books App!"}


@app.get("/books")
def get_books():
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return find_book(book_id)


@app.post("/books", status_code=201)
def create_book(data: BookCreate):
    global next_id
    book = {"id": next_id, **data.model_dump()}
    next_id += 1
    books.append(book)
    return book


@app.patch("/books/{book_id}")
def update_book(book_id: int, data: BookUpdate):
    book = find_book(book_id)
    book.update(data.model_dump(exclude_unset=True))
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    books.remove(book)
    return {"message": "Книга удалена"}

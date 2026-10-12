from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Хоббит", "author": "Джон Толкин"},
    {"id": 2, "title": "Маленький принц", "author": "Антуан де Сент-Экзюпери"},
]


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

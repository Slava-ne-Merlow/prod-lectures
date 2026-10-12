from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Привет, Books App!"}


@app.get("/books")
def get_books():
    return []

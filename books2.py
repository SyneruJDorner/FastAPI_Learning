from email import header
from optparse import Option
from urllib import response
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from starlette.responses import JSONResponse

class NegativeNumberExceptopn(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(title="Description of the book",
                            max_length=255,
                            min_length=1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        '''
        Create predefined data within a request body for swagger documentation
        '''
        schema_extra = {
            "example": {
                "id": "f9e8f8b0-f9e8-f9e8-f9e8-f9e8f9e8f9e8",
                "title": "Computer Science Pro",
                "author": "Codingwithroby",
                "description": "A very nice description of a book",
                "rating": 75
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(title="Description of the book",
                            max_length=255,
                            min_length=1)


BOOKS = []

@app.exception_handler(NegativeNumberExceptopn)
async def negative_number_handler(request: Request, exception: NegativeNumberExceptopn):
    return JSONResponse(status_code=418, content={"message": f'The number of books cannot be negative. provided value: {exception.books_to_return}'})


@app.post("/books/login/")
async def books_login(book_id: int, username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == "admin" and password == "admin":
        return BOOKS[book_id]
    return 'Invalid User'

@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Random-Header": random_header }

@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberExceptopn(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_books_no_api()
    
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS

@app.get("/book/{book_id}", )
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()

@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID: {book_id} deleted!'
    raise raise_item_cannot_be_found_exception()

def create_books_no_api():
    book_1 = Book(id=UUID('b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b9'),
                  title='The Great Gatsby',
                  author='F. Scott Fitzgerald',
                  description='The Great Gatsby is a 1925 novel written by American author F. Scott Fitzgerald.',
                  rating=60)
    book_2 = Book(id=UUID('b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b8'),
                    title='The Catcher in the Rye',
                    author='J. D. Salinger',
                    description='The Catcher in the Rye is a 1951 novel by J. D. Salinger. It is considered one of his best works and constitutes his best-known novel.',
                    rating=80)
    book_3 = Book(id=UUID('b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b7'),
                    title='Harry Potter and the Philosopher\'s Stone',
                    author='J. K. Rowling',
                    description='Harry Potter and the Philosopher\'s Stone is a fantasy novel written by British author J. K.',
                    rating=90)
    book_4 = Book(id=UUID('b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b6'),
                    title='The Hobbit',
                    author='J. R. R. Tolkien',
                    description='The Hobbit, or There and Back Again is a children\'s fantasy novel by English author J. R. R. Tolkien.',
                    rating=100)
    book_5 = Book(id=UUID('b9b9b9b9-b9b9-b9b9-b9b9-b9b9b9b9b9b5'),
                    title='The Lord of the Rings',
                    author='J. R. R. Tolkien',
                    description='The Lord of the Rings is a fantasy novel by English author J. R. R. Tolkien.',
                    rating=100)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
    BOOKS.append(book_5)

def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="Book not found", headers={"X-Header-Error": "Nothing found with the provided UUID."})
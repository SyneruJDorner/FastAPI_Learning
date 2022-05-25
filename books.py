from fastapi import FastAPI
from typing import Optional
from enum import Enum

app = FastAPI()

BOOKS = {
    'book_1': { 'title': 'Title One', 'author': 'Author One' },
    'book_2': { 'title': 'Title Two', 'author': 'Author Two' },
    'book_3': { 'title': 'Title Three', 'author': 'Author Three' },
    'book_4': { 'title': 'Title Four', 'author': 'Author Four' },
    'book_5': { 'title': 'Title Five', 'author': 'Author Five' },
}

class DirectionName(str, Enum):
    north = 'North'
    south = 'South'
    east = 'East'
    west = 'West'

@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_book = BOOKS.copy()
        del new_book[skip_book]
        return new_book
    return BOOKS

@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]

@app.post("/")
async def create_book(book_title: str, book_author: str):
    current_book_id = int(len(BOOKS.keys()))
    BOOKS[f'book_{current_book_id + 1}'] = { 'title': book_title, 'author': book_author }
    return BOOKS[f'book_{current_book_id + 1}']

@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = { 'title': book_title, 'author': book_author }
    BOOKS[book_name] = book_information
    return book_information

@app.delete("/{book_name}")
async def delete_book(book_name: str):
    del BOOKS[book_name]
    return f'Book_{book_name} deleted.'

@app.get("/books/mybook")
async def read_favourite_book():
    return { "book_title": "My favourite book" }

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return { "book_title": book_id }

@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return { "direction": direction_name, "sub": "Up" }
    elif direction_name == DirectionName.south:
        return { "direction": direction_name, "sub": "Down" }
    elif direction_name == DirectionName.east:
        return { "direction": direction_name, "sub": "Right" }
    elif direction_name == DirectionName.west:
        return { "direction": direction_name, "sub": "Left" }

@app.get("/assignment/")
async def read_book_assignment(book_name: str):
    return BOOKS[book_name]

@app.delete("/assignment/")
async def delete_book_assignment(book_name: str):
    del BOOKS[book_name]
    return BOOKS
import email
from email.policy import default
from msilib import schema
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("Todos", back_populates="owner")


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")

'''
sqlite3 todos.db

.schema

CREATE TABLE todos (
    id INTEGER NOT NULL,
    title VARCHAR,
    description VARCHAR,
    priority INTEGER,
    complete BOOLEAN,
    PRIMARY KEY (id)
);

CREATE INDEX ix_todos_id ON todos (id);

INSERT INTO todos (title, description, priority, complete) VALUES ('Go to the store', 'Pick up egss', 5, False);

SELECT * FROM todos;

INSERT INTO todos (title, description, priority, complete) VALUES ('Cut the lawn', 'Grass is getting long', 3, False);

SELECT * FROM todos;

INSERT INTO todos (title, description, priority, complete) VALUES ('Feed the dog', 'He is getting hungry', 5, False);

.mode column
SELECT * FROM todos;

.mode markdown
SELECT * FROM todos;

.mode box
SELECT * FROM todos;

.mode table
SELECT * FROM todos;

INSERT INTO todos (title, description, priority, complete) VALUES ('Test element', 'This is a test', 1, False);
SELECT * FROM todos;

DELETE FROM todos where id = 4;
SELECT * FROM todos;

INSERT INTO todos (title, description, priority, complete) VALUES ('Test element', 'This is a test', 1, False);
SELECT * FROM todos;

DELETE FROM todos where id = 4;
SELECT * FROM todos;
.quit
'''


'''
sqlite3 todos.db
.schema

DROP TABLE todos;

.schema
.quit
'''
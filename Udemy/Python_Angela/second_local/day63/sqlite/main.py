# import sqlite3
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

os.chdir("./Udemy/Python_Angela/second_local/day63/sqlite")
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# # cursor.execute(
# #     "CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)"
# # )

# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.9')")
# db.commit()

app = Flask(__name__)
app.secret_key = "lkjsldkjfksdf454854dfs"

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://" + file_path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app=app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __init__(self, id, title, author, rating):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating

    def __repr__(self):
        return f"<Book {self.title}>"


with app.app_context():

    db.create_all()

    new_book = Book(id=1, title="Harry Potter2", author="J. K. Rowling", rating=9.3)
    db.session.add(new_book)
    db.session.commit()

# if __name__ == "__main__":
#     app.run(debug=True)

# import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
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

    def __init__(self, title, author, rating):
        # self.id = id
        self.title = title
        self.author = author
        self.rating = rating

    def __repr__(self):
        return f"<Book {self.title}>"


with app.app_context():

    db.create_all()


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"],
        )
        with app.app_context():
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("add.html")


# with app.app_context():
#     new_book = Book(id=2, title="Harry Potter3", author="J. K. Rowling", rating=9.9)
#     db.session.add(new_book)
#     db.session.commit()

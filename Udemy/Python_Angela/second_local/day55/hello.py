from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return (
        "<h1 style='text-align: center'>Hello, World!</h1>"
        "<p>This is a paragraph.</p>"
        "<img src='https://media.giphy.com/media/l1AsTtnAciIpMmLcI/giphy.gif' width=200>"
    )


@app.route("/bye")
def say_bye():
    return "Bye"


@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello {name}! your {number} years old!"


if __name__ == "__main__":
    app.run(debug=True)

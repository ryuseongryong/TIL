from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return (
        "<h1 style='text-align: center'>Hello, World!</h1>"
        "<p>This is a paragraph.</p>"
        "<img src='https://media.giphy.com/media/l1AsTtnAciIpMmLcI/giphy.gif' width=200>"
    )


def make_bold(func):
    def wrapper():
        return f"<b>{func()}</b>"

    return wrapper


def make_emphasis(func):
    def wrapper():
        return f"<em>{func()}</em>"

    return wrapper


def make_underlined(func):
    def wrapper():
        return f"<u>{func()}</u>"

    return wrapper


@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "Bye"


@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello {name}! your {number} years old!"


if __name__ == "__main__":
    app.run(port=8000, debug=True)

from flask import Flask, render_template
import random
import datetime

app = Flask(__name__)


@app.route("/")
def home():
    # return "Hello World!"
    random_number = random.randint(1, 10)
    current_year = datetime.datetime.now().year
    return render_template("index.html", num1=random_number, year=current_year)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, flash, redirect, render_template, request, session
from flask_session.__init__ import Session

app = Flask(__name__)

#session
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/agregar")
def agregar():
    return render_template("agregar.html")

if __name__ == "__main__":
    app.run()
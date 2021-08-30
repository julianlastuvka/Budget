from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'thisisatemporarykey849489849489489+4'
app.config['SESSION_TYPE'] = 'filesystem'
app.config["TEMPLATES_AUTO_RELOAD"] = True

Session(app)

db = SQL("sqlite:///budget-db.db")

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET 
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        #check if a username was provided
        if not request.form.get("username"):
            return render_template("register.html")

        #check that a password was provided
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return render_template("register.html")

        #check that the password and password confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html")
        
        #get all users's usernames
        users = db.execute("SELECT username from users")

        # checks if the username is available
        if any(request.form.get("username") in d.values() for d in users):
            return render_template("register.html")
        # Register the user :)
        else:
            db.execute("INSERT into users (username, email, hash) VALUES(?,?,?)", request.form.get(
                "username"),request.form.get("email"), generate_password_hash(request.form.get("password")))

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return render_template("index.html")

@app.route("/agregar")
@login_required
def agregar():
    return render_template("agregar.html")

if __name__ == "__main__":
    app.run()
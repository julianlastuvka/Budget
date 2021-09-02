from flask import Flask, flash, redirect, render_template, request, session,url_for
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




@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    username = session["username"]
    rows = db.execute("SELECT * from history WHERE id = ?", session["user_id"])

    return render_template("index.html", username=username, rows=rows)




@app.route("/agregar", methods=["GET", "POST"])
@login_required
def agregar():

    if request.method == "POST":
        nombre_gasto = request.form.get("nombre_gasto")
        categoria = request.form.get("cat")
        subcat = request.form.get("sub_cat")
        fecha = request.form.get("fecha")
        precio = request.form.get("precio")
        cantidad = request.form.get("cant")

        #checking for blank fields.
        if not nombre_gasto or not categoria or not subcat or not fecha or not precio or not cantidad:
            # TO DO 
            # MESSAGE: ONE OR MORE FIELDS LEFT BLANK
            return render_template("agregar.html")
        # --------------------------------------------------------
        # check for valid precio and cantidad
        try:
            precio = float(precio)
            cantidad = float(cantidad)
        except ValueError:
            # TODO
            # ERROR MESSAGE: INVALID PRICE OR QUANTITY
            return render_template("agregar.html")
        # --------------------------------------------------------
        # check for valid fecha
        try:
            dia = int(fecha[0:2])
            mes = int(fecha[3:5])
            anio = int(fecha[6:8])
        except:
            ## TODO
            ## ERROR MESSAGE: INVALID DATE
            return render_template("agregar.html")

        db.execute("INSERT INTO history VALUES (?,?,?,?,?,?,?,?,?)", session["user_id"], nombre_gasto, categoria, subcat, cantidad, precio, fecha[0:2], fecha[3:5], fecha[6:8])
        # TODO
        # return success message
        return render_template("agregar.html", nombre_gasto=nombre_gasto)

    else:
        return render_template("agregar.html")

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
        session["username"] = rows[0]["username"]

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


if __name__ == "__main__":
    app.run()
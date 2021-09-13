from flask import Flask, flash, redirect, render_template, request, session,url_for
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

from datetime import datetime


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

def procesar_gastos_mensuales(rows):
    j = 0
    gastos_diarios_del_mes = {}

    for dia in range(1,32):
    
        total_dia = 0
        while rows[j]["dia"] == dia:
        
            total_dia += int(rows[j]["precio"])
        
            if j < len(rows) - 1:
                j+= 1
            else:
                break
        
        gastos_diarios_del_mes[dia] = total_dia 

    return gastos_diarios_del_mes




@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    gastos_mensuales = {}
    if request.method == "POST":

        anio = request.form.get("anio")
        mes = request.form.get("mes")
        dia = request.form.get("dia")

        #CHECK FOR VALID INPUT / TODO

        #Daily history

        if anio and mes and dia:
            rows = db.execute("SELECT * from history WHERE id = ? AND anio = ? AND mes = ? AND dia = ?", session["user_id"], anio, mes, dia)
        
        elif anio and mes:
            rows = db.execute("SELECT dia, mes, precio from history WHERE id = ? AND anio = ? AND mes = ? ORDER BY dia", session["user_id"], anio, mes)

            gastos_mensuales = procesar_gastos_mensuales(rows)



        elif anio:
            rows = db.execute("SELECT * from history WHERE id = ? AND anio = ?", session["user_id"], anio)
            print("\n\n", rows)

        

        return render_template("index.html", rows=rows, dia=dia, mes=mes, anio=anio, gastos_mensuales=gastos_mensuales)

    date = datetime.now()
    anio, mes, dia = date.year, date.month, date.day
    rows = db.execute("SELECT * from history WHERE id = ? AND anio = ? AND mes = ?", session["user_id"], anio, mes)
    
    return render_template("index.html", rows=rows, anio=anio, mes=mes, dia=dia)




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
            anio = int(fecha[6:10])
        except:
            ## TODO
            ## ERROR MESSAGE: INVALID DATE
            return render_template("agregar.html")

        db.execute("INSERT INTO history VALUES (?,?,?,?,?,?,?,?,?)", session["user_id"], nombre_gasto, categoria, subcat, cantidad, precio, dia, mes, anio)
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
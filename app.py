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

NOMBRE_A_NUMERO_DE_MES = {
    "Enero": 1,
    "Febrero": 2,
    "Marzo": 3,
    "Abril": 4,
    "Mayo": 5,
    "Junio": 6,
    "Julio": 7,
    "Agosto": 8,
    "Septiembre": 9,
    "Octubre": 10,
    "Noviembre": 11,
    "Diciembre": 12
}

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def procesar_gastos_diarios(rows):

    gasto_total_dia = 0
    for row in rows:
        gasto_total_dia += float(row["precio"]) 

    return gasto_total_dia

def procesar_gastos_mensuales(gastos_del_mes):

    if not gastos_del_mes:
        return {}, 0
    j = 0
    gastos_diarios_del_mes = {}
    gasto_total_mes = 0

    for dia in range(1,32):
    
        total_dia = 0

        while gastos_del_mes[j]["dia"] == dia:
        
            total_dia += int(gastos_del_mes[j]["precio"])
        
            if j < len(gastos_del_mes) - 1:
                j+= 1
            else:
                break
        
        gastos_diarios_del_mes[dia] = total_dia 
        gasto_total_mes += total_dia

    return gastos_diarios_del_mes, gasto_total_mes



def procesar_gastos_anuales(anio):

    gastos_totales_de_cada_mes = {}
    gasto_total_anio = 0

    for mes in range(1, 13):

        gastos_del_mes = db.execute("SELECT dia, precio FROM history WHERE id = ? AND anio = ? AND mes = ? ORDER BY dia", session["user_id"], anio, mes)

        if gastos_del_mes:
            n, gasto_total_mes = procesar_gastos_mensuales(gastos_del_mes)
        else:
            gasto_total_mes = 0

        gastos_totales_de_cada_mes[mes] = gasto_total_mes
        gasto_total_anio += gasto_total_mes

    return gastos_totales_de_cada_mes, gasto_total_anio
    



@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    presupuesto_anual = db.execute("SELECT budget FROM users WHERE id = ?", session["user_id"])[0]["budget"]

    if request.method == "POST":

        anio = request.form.get("anio")
        nombre_de_mes = request.form.get("mes")
        dia = request.form.get("dia")

        if nombre_de_mes:
            mes = NOMBRE_A_NUMERO_DE_MES[nombre_de_mes]
        else:
            mes = None

        #Daily history
        if anio and mes and dia:
            rows = db.execute("SELECT * from history WHERE id = ? AND anio = ? AND mes = ? AND dia = ?", session["user_id"], anio, mes, dia)

            gasto_total_dia = procesar_gastos_diarios(rows)
            
            if not gasto_total_dia:
                gasto_total_dia = "No hay gastos registrados en el día seleccionado."

            return render_template("index.html", dia=dia, mes=mes, anio=anio, gasto_total_dia=gasto_total_dia, rows=rows, nombre_de_mes=nombre_de_mes, presupuesto_anual=presupuesto_anual)
        
        # Montly history
        elif anio and mes:
            rows = db.execute("SELECT dia, precio from history WHERE id = ? AND anio = ? AND mes = ? ORDER BY DIA", session["user_id"], anio, mes)
            
            gastos_mensuales, gasto_total_mes = procesar_gastos_mensuales(rows)

            print(f"\n\n\n {gastos_mensuales} \n\n\n")

            if not gastos_mensuales:
                gastos_mensuales = "No hay gastos registrados en el mes seleccionado."
            
            return render_template("index.html", rows=rows, anio=anio, mes=mes, dia=dia, gastos_mensuales=gastos_mensuales, gasto_total_mes=gasto_total_mes, nombre_de_mes=nombre_de_mes, presupuesto_anual=presupuesto_anual)

        # Yearly history
        elif anio:
            gastos_por_mes, gasto_total_anio = procesar_gastos_anuales(anio)

            if not gasto_total_anio:
                gasto_total_anio = "No hay gastos registrados en el año seleccionado."

            return render_template("index.html", dia=dia, mes=mes, anio=anio, gastos_por_mes=gastos_por_mes, gasto_total_anio=gasto_total_anio, presupuesto_anual=presupuesto_anual)


    date = datetime.now()
    anio, mes, dia = date.year, date.month, date.day
    nombre_de_mes = ""
    rows = db.execute("SELECT dia, precio from history WHERE id = ? AND anio = ? AND mes = ? ORDER BY dia", session["user_id"], anio, mes)
    gastos_mensuales, gasto_total_mes = procesar_gastos_mensuales(rows)


    return render_template("index.html", rows=rows, anio=anio, mes=mes, dia=dia, gastos_mensuales=gastos_mensuales, gasto_total_mes=gasto_total_mes, nombre_de_mes=nombre_de_mes, presupuesto_anual=presupuesto_anual)




@app.route("/agregar", methods=["GET", "POST"])
@login_required
def agregar():

    presupuesto_anual = db.execute("SELECT budget FROM users WHERE id = ?", session["user_id"])[0]["budget"]

    if request.method == "POST":
        nombre_gasto = request.form.get("nombre_gasto")
        categoria = request.form.get("cat")
        precio = request.form.get("precio")
        dia = request.form.get("dia")
        nombre_de_mes = request.form.get("mes")
        anio = request.form.get("anio")

        if nombre_de_mes:
            mes = NOMBRE_A_NUMERO_DE_MES[nombre_de_mes]
        else:
            mes = None

        #checking for blank fields.
        if not nombre_gasto or not categoria or not dia or not mes or not precio or not anio:
            # MESSAGE: ONE OR MORE FIELDS LEFT BLANK
            error_message = "Error: Uno o más campos fueron dejados en blanco."
            return render_template("agregar.html", error_message=error_message, presupuesto_anual=presupuesto_anual)
        # --------------------------------------------------------
        # check for valid precio

        if precio[0] == "$":
            precio = precio[1:]

        try:
            precio = float(precio)

        except ValueError:
            # ERROR MESSAGE: INVALID PRICE
            error_message = "Error: Precio inválido. Utilice caracteres numéricos."
            return render_template("agregar.html", error_message=error_message, presupuesto_anual=presupuesto_anual)
        # --------------------------------------------------------

        db.execute("INSERT INTO history VALUES (?,?,?,?,?,?,?)", session["user_id"], nombre_gasto, categoria, precio, dia, mes, anio)
        # return success message
        success_message = f"Gasto '{nombre_gasto}' agregado exitosamente :)"
        return render_template("agregar.html", nombre_gasto=nombre_gasto, success_message=success_message, presupuesto_anual=presupuesto_anual)

    else:
        return render_template("agregar.html", presupuesto_anual=presupuesto_anual)


@app.route("/cuenta", methods=["GET", "POST"])
@login_required
def cuenta():

    success_message = ""
    error_message = ""

    if request.method == "POST":

        nueva_contraseña = request.form.get("contraseña")
        presupuesto = request.form.get("presupuesto")

        if presupuesto:
            try:
                presupuesto = int(presupuesto)
                db.execute("UPDATE users SET budget = ? WHERE id = ?", presupuesto, session["user_id"])
                success_message= "Presupuesto actualizado correctamente"
            except:
                error_message = "Error: Introduzca un entero para el nuevo presupuesto."
            
        elif nueva_contraseña:
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(nueva_contraseña), session["user_id"])
            success_message= "Contraseña actualizada correctamente"

        else:
            error_message = "Error: Complete el campo antes de enviar/cambiar."

    return render_template("cuenta.html", success_message=success_message, error_message=error_message)




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username or not password:
            error_message = "Introduzca un nombre de usuario y contraseña."
            return render_template("login.html", error_message=error_message)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            error_message = "El usuario o la contraseña no son correctos."
            return render_template("login.html", error_message=error_message)

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

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        presupuesto = request.form.get("presupuesto")

        if not presupuesto:
            presupuesto = 0

        if not username or not password or not email:
            # ERROR MESSAGE
            error_message = "Complete los campos de usuario, email y contraseña."
            return render_template("register.html", error_message=error_message)

        #get all users's usernames
        users = db.execute("SELECT username from users")

        # checks if the username is available
        if any(request.form.get("username") in d.values() for d in users):
            error_message = "EL nombre de usuario se encuentra en uso. Intente con uno diferente."
            return render_template("register.html", error_message=error_message)

        # Register the user :)
        else:
            db.execute("INSERT into users (username, email, hash, budget) VALUES(?,?,?,?)", username, email, generate_password_hash(password), presupuesto)

        return redirect("/login")

    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run()
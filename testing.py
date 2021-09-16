from app import procesar_gastos_anuales
from cs50 import SQL

rows = [{'dia': 1, 'mes': 4, 'precio': 1000},
        {'dia': 2, 'mes': 4, 'precio': 600},
        {'dia': 10, 'mes': 5, 'precio': 630},
        {'dia': 20, 'mes': 6, 'precio': 500},
        {'dia': 22, 'mes': 6, 'precio': 700},
        {'dia': 20, 'mes': 7, 'precio': 500}]


db = SQL("sqlite:///budget-db.db")


def procesar_gastos_mensuales(rows):
    
    j = 0
    gastos_diarios_del_mes = {}
    gasto_total_mes = 0
    for dia in range(1,32):
    
        total_dia = 0
        while rows[j]["dia"] == dia:
        
            total_dia += int(rows[j]["precio"])
        
            if j < len(rows) - 1:
                j+= 1
            else:
                break
        
        gastos_diarios_del_mes[dia] = total_dia 
        gasto_total_mes += total_dia

    return gastos_diarios_del_mes, gasto_total_mes

def procesar_gastos_anuales(anio):

    gastos_por_mes = {}
    gasto_total_anio = 0

    for mes in range(1, 13):

        row = db.execute("SELECT * FROM history WHERE id = ? AND anio = ? AND mes = ?", session["user_id"], anio, mes)

        n, gasto_total_mes = procesar_gastos_mensuales(row)

        gastos_por_mes[mes] = gasto_total_mes
        gasto_total_anio += gasto_total_mes

    return gastos_por_mes, gasto_total_anio
rows =[{'id': 1, 'nombre_gasto': 'vacio', 'categoria': 'carne', 'precio': 600, 'dia': 9, 'mes': 9, 'anio': 2021}, {'id': 1, 'nombre_gasto': 'sadfsadf', 'categoria': 'comida', 'precio': 390, 'dia': 12, 'mes': 9, 'anio': 2021}, {'id': 1, 'nombre_gasto': 'vacio', 'categoria': 'carne', 'precio': 600, 'dia': 10, 'mes': 9, 'anio': 2021}, {'id': 1, 'nombre_gasto': 'auriculares', 'categoria': 'tecnologia', 'precio': 1200, 'dia': 6,
'mes': 9, 'anio': 2021}, {'id': 1, 'nombre_gasto': 'auriculares', 'categoria': 'tecnologia', 'precio': 1200, 'dia': 6, 'mes': 9, 'anio': 2021}, {'id': 1, 'nombre_gasto': 'papel higienico', 'categoria': 'higiene', 'precio': 150, 'dia': 12, 'mes': 9, 'anio': 2021}, {'id': 1, 'nombre_gasto': 'ejemplo2', 'categoria': 'ejemplo', 'precio': 2222, 'dia': 1, 'mes': 9, 'anio': 2021}, {'id': 1, 'nombre_gasto': 'ejemplo', 'categoria': 'ejemplo', 'precio': 111, 'dia': 1, 'mes': 9, 'anio': 2021}]


def procesar_gastos_mensuales(rows):

    if not rows:
        return {}, 0
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


a, b = procesar_gastos_mensuales(rows)

print(a, b)
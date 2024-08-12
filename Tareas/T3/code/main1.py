# TAREA 3
# Jacinta Ortiz y Vicente Lavagnino

# Pregunta 3.1

## ______________________ CSV ______________________ ##
import pandas as pd
from gurobipy import GRB, Model, quicksum

# PARAMETROS

peso = []
estatura = []
edad = []
contorno_cabeza = []
distancia_hombro_cuello = []
altura_cuello = []
contorno_cuello = []
altura_cabeza = []
peso_cabeza = []
distancia_hombro_cabeza = []
contorno_caja_toraxica = []
contorno_brazo  = []
largo_del_brazo = []
distancia_menton_oreja = []
ancho_cabeza = []
gramos_relleno = []

# MUESTRA CSV
muestra = pd.read_csv("muestras.csv", header=0).values.tolist()

for i in range(len(muestra)):
    peso.append(muestra[i][0])
    estatura.append(muestra[i][1])
    edad.append(muestra[i][2])
    contorno_cabeza.append(muestra[i][3])
    distancia_hombro_cuello.append(muestra[i][4])
    altura_cuello.append(muestra[i][5])
    contorno_cuello.append(muestra[i][6])
    altura_cabeza.append(muestra[i][7])
    peso_cabeza.append(muestra[i][8])
    distancia_hombro_cabeza.append(muestra[i][9])
    contorno_caja_toraxica.append(muestra[i][10])
    contorno_brazo.append(muestra[i][11])
    largo_del_brazo.append(muestra[i][12])
    distancia_menton_oreja.append(muestra[i][13])
    ancho_cabeza.append(muestra[i][14])
    gramos_relleno.append(muestra[i][15])

encuestados = len(peso)

## ______________________ GUROBI ______________________ ##

# Generacion del modelo
model = Model("Ejercicio 3.1")
model.setParam("TimeLimit", 60)  # Tiempo maximo en segundos

# Se instancian variables de decision
b = model.addVar(vtype=GRB.CONTINUOUS, name="b")
w_i = model.addVars(15, vtype=GRB.CONTINUOUS, name="w_i")

#------------------ Agregar las variables al modelo -------------------
model.update()

#------------------------- Funcion Objetivo ---------------------------
objetivo = quicksum((b + quicksum(w_i[j] * muestra[i][j] for j in range(15)) - gramos_relleno[i]) ** 2 for i in range(encuestados))
model.setObjective(objetivo, GRB.MINIMIZE)

# Optimizar el modelo
model.optimize()

if model.status == GRB.OPTIMAL:
    b_opt = b.X
    w_opt = [w_i[i].X for i in range(15)]

    columnas = [
        "peso", "estatura", "edad", "contorno_cabeza", "distancia_hombro_cuello", 
        "altura_cuello", "contorno_cuello", "altura_cabeza", "peso_cabeza", 
        "distancia_hombro_cabeza", "contorno_caja_toraxica", "contorno_brazo", 
        "largo_del_brazo", "distancia_menton_oreja", "ancho_cabeza"
    ]
    
    for j in range(15):
        print(f'{columnas[j]}: {w_opt[j]}')

    print(f'b: {b_opt}')
    print(f'Función objetivo: {model.objVal}')
else:
    print("No se encontró una solución óptima.")

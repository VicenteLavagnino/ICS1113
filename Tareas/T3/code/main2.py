# TAREA 3
# Jacinta Ortiz y Vicente Lavagnino

# Pregunta 3.2

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
model = Model("Ejercicio 3.2")
model.setParam("TimeLimit", 60)  # Tiempo maximo en segundos

λ = int(input("Ingrese el valor de λ: "))

# Se instancian variables de decision
b = model.addVar(vtype=GRB.CONTINUOUS, name="b")
w_i = model.addVars(15, vtype=GRB.CONTINUOUS, name="w_i")
z_i = model.addVars(15, vtype=GRB.CONTINUOUS, name="z_i")

#------------------ Agregar las variables al modelo -------------------
model.update()

#------------------------- Funcion Objetivo ---------------------------
objetivo = quicksum((b + quicksum(w_i[j] * muestra[i][j] for j in range(15)) - gramos_relleno[i]) ** 2 for i in range(encuestados)) + λ * quicksum(z_i[j] for j in range(15))
model.setObjective(objetivo, GRB.MINIMIZE)


#------------------------- Restricciones ---------------------------
for j in range(15):
    model.addConstr(-z_i[j] <= w_i[j], name=f"R1")
    model.addConstr(w_i[j] <= z_i[j], name=f"R2")

# Optimizar el modelo
model.optimize()

if model.status == GRB.OPTIMAL:
    b_sol = b.X
    w_sol = [w_i[i].X for i in range(15)]
    z_sol = [z_i[j].X for j in range(15)]

    columnas = [
        "peso", "estatura", "edad", "contorno_cabeza", "distancia_hombro_cuello", 
        "altura_cuello", "contorno_cuello", "altura_cabeza", "peso_cabeza", 
        "distancia_hombro_cabeza", "contorno_caja_toraxica", "contorno_brazo", 
        "largo_del_brazo", "distancia_menton_oreja", "ancho_cabeza"
    ]
    
    for j in range(15):
        print(f'{columnas[j]}: {w_sol[j]}')
        # print(f'Valor Absoluto: {z_sol[j]}')

    print(f'b: {b_sol}')
    print(f"Valor λ: {λ}")

    print("\n")
    print("Los 5 ponderadores más importantes son:")

    mejores = []

    for j in range(15):
        mejores.append((columnas[j], w_sol[j]))
    
    mejores.sort(key=lambda x: x[1], reverse=False)

    for i in range(5):
        print(f"{mejores[i][0]}: {mejores[i][1]}")

    print(f'Función objetivo: {model.objVal}')

else:
    print("No se encontró una solución óptima.")

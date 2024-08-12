# TAREA 2
# Jacinta Ortiz y Vicente Lavagnino

# Pregunta 3

## ______________________ CSV ______________________ ##
import pandas as pd

# CANTIDAD CUADRANTES
cuadrantes = pd.read_csv("cantidad_cuadrantes.csv", header=None).values.tolist()
cuadrantes = int(cuadrantes[0][0])
#print(cuadrantes)

# CAPACIDAD POR SACO
capacidad_por_saco = pd.read_csv("capacidad_por_saco.csv", header=None).values.tolist()

for i in range(len(capacidad_por_saco)):
    capacidad_por_saco[i] = int(capacidad_por_saco[i][0])
#print(capacidad_por_saco)

# CAPITAL INICIAL
capital_inicial = pd.read_csv("capital_inicial.csv", header=None).values.tolist()
capital_inicial = int(capital_inicial[0][0])
#print(capital_inicial)

# COSTO POR SACO HACERRRR
costos_por_saco = pd.read_csv("costo_saco.csv", header=None).values.tolist()
#print(costos_por_saco)

# KILOS FRUTA
kilos_fruta = pd.read_csv("kilos_fruta.csv", header=None).values.tolist()

for i in range(len(kilos_fruta)):
    kilos_fruta[i] = int(kilos_fruta[i][0])
#print(kilos_fruta)

# PRECIO VENTA HACERRRR
precio_venta = pd.read_csv("precio_venta.csv", header=None).values.tolist()
#print(precio_venta)


# TIEMPO DEMORA
tiempo_demora = pd.read_csv("tiempo_demora.csv", header=None).values.tolist()

for i in range(len(tiempo_demora)):
    tiempo_demora[i] = int(tiempo_demora[i][0])
#print(tiempo_demora)


## ______________________ GUROBI ______________________ ##

from gurobipy import GRB, Model

#---------------------- Generacion del modelo ------------------------
model = Model()
model.setParam("TimeLimit", 60)  # Tiempo maximo en segundos

#---------------- Se instancian variables de decision -----------------

# Cantidades
J = len(kilos_fruta) # Cantidad de semillas
K = cuadrantes # Cantidad de cuadrantes
T = len(costos_por_saco[0]) # Cantidad de tiempos

x = model.addVars(J, K, T, vtype=GRB.BINARY, name="x")
y = model.addVars(J, K, T, vtype=GRB.BINARY, name="y")
i = model.addVars(T, vtype=GRB.CONTINUOUS, name="i")
u = model.addVars(J, T, vtype=GRB.INTEGER, name="u")
w = model.addVars(J, T, vtype=GRB.INTEGER, name="w")

#------------------ Agregar las variables al modelo -------------------
model.update()

#----------------------- Agregar Restricciones ------------------------

# Restriccion 1
for j in range(J):
    for k in range(K):
        for t in range(T):
            model.addConstr(sum(y[j, k, l] for l in range(t, min(t + tiempo_demora[j], T))) >= tiempo_demora[j] * x[j, k, t], "Activacion sembrado")

# Restriccion 2
for k in range(K):
    for t in range(T):
        model.addConstr(sum(y[j, k, t] for j in range(J)) <= 1, "Solo 1 sembrado por cuadrante")

# Restriccion 3
for t in range(1, T):
    model.addConstr(i[t] == i[t - 1] - sum(costos_por_saco[j][t] * w[j, t] for j in range(J)) + sum(x[j, k, t - tiempo_demora[j]] * kilos_fruta[j] * precio_venta[j][t] for j in range(J) for k in range(K) if t - tiempo_demora[j] >= 0), "Inventario de dinero")


# Restriccion 4
model.addConstr(i[0] == capital_inicial - sum(costos_por_saco[j][0] * w[j, 0] for j in range(J)), "Condicion borde inventario dinero")


# Restriccion 5
for j in range(J):
    for t in range(1, T):
        model.addConstr(u[j, t] == u[j, t - 1] + capacidad_por_saco[j] * w[j, t] - sum(x[j, k, t] for k in range(K)), "Inventario semillas")

# Restriccion 6
for j in range(J):
    model.addConstr(u[j, 0] == capacidad_por_saco[j] * w[j, 0] - sum(x[j, k, 0] for k in range(K)), "Condicion borde semillas")

# Restriccion 7
for j in range(J):
    for k in range(K):
        for t in range(T - 1):
            model.addConstr(1 - x[j, k, t] >= sum(x[j, k, l] for l in range(t + 1, min(t + tiempo_demora[j], T))), "Terminar cosecha antes de volver a cosechar")

# Naturaleza de las Variables
for t in range(T):
    model.addConstr(i[t] >= 0, "Inventario de dinero positivo")

for j in range(J):
    for t in range(T):
        model.addConstr(u[j,t] >= 0, "positivo")
        model.addConstr(w[j,t] >= 0, "positivo")

#------------------------- Funcion Objetivo ---------------------------
objetivo = i[T - 1]
model.setObjective(objetivo, GRB.MAXIMIZE)
model.optimize()

#------------------------ Manejo Soluciones --------------------------\\
print("\n --------- SOLUCIÓN --------- \n")
print("Valor Objetivo (en pesos): ", int(model.objVal))


print("\n --------- PLANTACIONES EN CADA CUADRANTE --------- \n")

for k in range(K):
        plantaciones = int(sum(x[j, k, t].X for j in range(J) for t in range(T)))
        print(f"En el cuadrante {k+1}: se plantó {plantaciones} veces")

print("\n --------- CALENDARIO --------- \n")

calendario = pd.DataFrame(index=range(K), columns=range(T))
    
for k in range(K):
        for t in range(T):
            semillas_plantadas = [j for j in range(J) if x[j, k, t].X > 0]
            if semillas_plantadas:
                calendario.at[k, t] = semillas_plantadas[0]
            else:
                calendario.at[k, t] = 0
print(calendario)

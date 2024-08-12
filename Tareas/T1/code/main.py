# TAREA 1
# Jacinta Ortiz y Vicente Lavagnino

# Pregunta 3
 
## ______________________ CSV ______________________ ##
import pandas as pd

# CONTENIDOS NUTRICIONALES
contenidos_nutricionales = pd.read_csv("contenidos_nutricionales.csv", header=None).values.tolist()[1:]
contenidos_nutricionales = [[float(value) for value in row] for row in contenidos_nutricionales]
# print(contenidos_nutricionales)

# COSTOS
costos = pd.read_csv("costos.csv", header=None).values.tolist()[1:]
costos = [float(row[0]) for row in costos]
# print(costos)

# LIMITES
limites = pd.read_csv("limites.csv", header=None).values.tolist()[1:]
limites = [[float(value) for value in row] for row in limites]
# print(limites)


## ______________________ GUROBI ______________________ ##

from gurobipy import GRB, Model

#----------------------- Generacion del modelo ------------------------
model = Model()
model.setParam("TimeLimit", 60) #Establece el tiempo maximo en segundos

#---------------- Se instancian variables de decision -----------------

# PROPORCION
x = model.addVars(len(costos),vtype = GRB.CONTINUOUS, name="x")

#------------------ Agregar las variables al modelo -------------------
model.update()

#----------------------- Agregar Restricciones ------------------------

# La mezcla esta compuesta unicamente por cereales
model.addConstr(sum(x[j] for j in range(len(costos))) == 1, "Total Valor Nutricional")


# Se debe cumplir una proporcion minixma de nutrientes
model.addConstrs((sum(contenidos_nutricionales[i][j] * x[j] for j in range(len(costos))) >= limites[i][0] for i in range(len(contenidos_nutricionales))), "Minimo Nutrientes")
# Se debe cumplir una proporcion minima de nutrientes
model.addConstrs((sum(contenidos_nutricionales[i][j] * x[j] for j in range(len(costos))) <= limites[i][1] for i in range(len(contenidos_nutricionales))), "Maximo Nutrientes")

# Naturaleza de las variables
model.addConstrs((x[j] >= 0 for j in range(len(costos))), "Nutrientes 0_positivos")

#------------------------- Funcion Objetivo ---------------------------

objetivo = sum(costos[j] * x[j] for j in range(len(costos)))
model.setObjective(objetivo, GRB.MINIMIZE)
model.optimize()

#------------------------ Manejo Soluciones -s--------------------------

print("\n"+"-"*10+" Manejo Soluciones "+"-"*10)
print(f"El valor objetivo es de: {model.ObjVal}")
for j in x:
    print(f"La variable x_{j} toma el valor de {x[j].x}")
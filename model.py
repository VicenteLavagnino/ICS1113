#----------------------- GUROBI ------------------------

from gurobipy import GRB, Model

#----------------------- Generacion del modelo ------------------------
model = Model()
model.setParam("TimeLimit", 3000) #Establece el tiempo maximo en segundos

#----------------------- Variables ------------------------


#----------------------- Restricciones ------------------------


#----------------------- Funcion objetivo ------------------------


#----------------------- Solucion ------------------------
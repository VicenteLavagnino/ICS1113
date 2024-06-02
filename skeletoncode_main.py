import gurobipy as gp
from gurobipy import GRB
import pandas as pd
from parameters import get_data

# Cargar datos desde parametros.py
A, P, B, R, I, Ep1_p2, Jp_b, Dp_r, Fp_b, Mp, Qb_r, Vp, L = get_data()

# Crear el modelo
model = gp.Model("Fundacion_Atrevete")

# Variables de decisión
Xa = model.addVars(A, vtype=GRB.BINARY, name="Xa")
Yp_r = model.addVars(P, R, vtype=GRB.BINARY, name="Yp_r")
Ta_p_i = model.addVars(A, P, I, vtype=GRB.BINARY, name="Ta_p_i")
Wa_b = model.addVars(A, B, vtype=GRB.BINARY, name="Wa_b")
Za_b_p_r = model.addVars(A, B, P, R, vtype=GRB.BINARY, name="Za_b_p_r")
Ha_p_i = model.addVars(A, P, I[:-1], vtype=GRB.BINARY, name="Ha_p_i")
Sa_p1_p2_i = model.addVars(A, P, P, I[:-1], vtype=GRB.BINARY, name="Sa_p1_p2_i")
Ua_b_p = model.addVars(A, B, P, vtype=GRB.BINARY, name="Ua_b_p")

# Función objetivo
model.setObjective(
    gp.quicksum(Sa_p1_p2_i[a, p1, p2, i] * Ep1_p2[(p1, p2)] for a in A for p1 in P for p2 in P for i in I[:-1] if (p1, p2) in Ep1_p2) +
    gp.quicksum(Ua_b_p[a, b, p] * Jp_b[(p, b)] for a in A for b in B for p in P if (p, b) in Jp_b),
    GRB.MINIMIZE
)

# Restricciones

# 1. Cada auto tiene a lo más un profesor en cada asiento
for a in A:
    for i in I:
        model.addConstr(gp.quicksum(Ta_p_i[a, p, i] for p in P) <= 1, name=f"Restriccion1_{a}_{i}")

# 2. Cada auto es activado si y solo si tiene a algún profesor dentro. Este profesor debe ir en el asiento 0 (asiento del conductor)
for a in A:
    model.addConstr(Xa[a] == gp.quicksum(Ta_p_i[a, p, 0] for p in P), name=f"Restriccion2_{a}")

# 3. Un auto está asociado a un bloque (y uno solo) si y solo si está activado
for a in A:
    model.addConstr(Xa[a] == gp.quicksum(Wa_b[a, b] for b in B), name=f"Restriccion3_{a}")

# 4. Cada auto solo puede tener a un profesor en el asiento i si hay un profesor en el asiento i-1
for a in A:
    for i in range(1, 5):
        model.addConstr(gp.quicksum(Ta_p_i[a, p, i] for p in P) <= gp.quicksum(Ta_p_i[a, p, i-1] for p in P), name=f"Restriccion4_{a}_{i}")

# 5. Si un profesor está en el asiento 0 de un auto, debe poder manejar
for a in A:
    for p in P:
        model.addConstr(Ta_p_i[a, p, 0] <= Mp[p], name=f"Restriccion5_{a}_{p}")

# 6. Cada profesor es asignado a un solo auto y a un solo asiento de este
for p in P:
    model.addConstr(gp.quicksum(Ta_p_i[a, p, i] for a in A for i in I) == 1, name=f"Restriccion6_{p}")

# 7. A cada profesor se le asigna un solo ramo
for p in P:
    model.addConstr(gp.quicksum(Yp_r[p, r] for r in R) == 1, name=f"Restriccion7_{p}")

# 8. El ramo al cual el profesor sea asignado debe ser uno de los ramos a los que postuló
for p in P:
    for r in R:
        model.addConstr(Yp_r[p, r] <= Dp_r[p, r], name=f"Restriccion8_{p}_{r}")

# 9. A cada bloque debe llegar la cantidad de profesores que se pidieron por ramo
for b in B:
    for r in R:
        model.addConstr(gp.quicksum(Za_b_p_r[a, b, p, r] for a in A for p in P) == Qb_r[b, r], name=f"Restriccion9_{b}_{r}")

# 10. Definición de la variable Sa_p1_p2_i
for a in A:
    for p1 in P:
        for p2 in P:
            for i in range(4):
                model.addConstr(Sa_p1_p2_i[a, p1, p2, i] <= Ta_p_i[a, p1, i], name=f"Restriccion10_1_{a}_{p1}_{p2}_{i}")
                model.addConstr(Sa_p1_p2_i[a, p1, p2, i] <= Ta_p_i[a, p2, i+1], name=f"Restriccion10_2_{a}_{p1}_{p2}_{i}")
                model.addConstr(Ta_p_i[a, p1, i] + Ta_p_i[a, p2, i+1] <= 1 + Sa_p1_p2_i[a, p1, p2, i], name=f"Restriccion10_3_{a}_{p1}_{p2}_{i}")

# 11. Definición de la variable Ha_p_i
for a in A:
    for p in P:
        for i in range(4):
            model.addConstr(Ha_p_i[a, p, i] <= Ta_p_i[a, p, i], name=f"Restriccion11_1_{a}_{p}_{i}")
            model.addConstr(Ha_p_i[a, p, i] <= 1 - gp.quicksum(Ta_p_i[a, p2, i+1] for p2 in P), name=f"Restriccion11_2_{a}_{p}_{i}")
            model.addConstr(Ta_p_i[a, p, i] - gp.quicksum(Ta_p_i[a, p2, i+1] for p2 in P) <= Ha_p_i[a, p, i], name=f"Restriccion11_3_{a}_{p}_{i}")

# 12. Definición de la variable Ua_b_p
for a in A:
    for b in B:
        for p in P:
            model.addConstr(Ua_b_p[a, b, p] <= Ta_p_i[a, p, 4] + gp.quicksum(Ha_p_i[a, p, i] for i in range(4)), name=f"Restriccion12_1_{a}_{b}_{p}")
            model.addConstr(Ua_b_p[a, b, p] <= Wa_b[a, b], name=f"Restriccion12_2_{a}_{b}_{p}")
            model.addConstr(Wa_b[a, b] + Ta_p_i[a, p, 4] <= Ua_b_p[a, b, p] + 1, name=f"Restriccion12_3_{a}_{b}_{p}")
            model.addConstr(Wa_b[a, b] + gp.quicksum(Ha_p_i[a, p, i] for i in range(4)) <= Ua_b_p[a, b, p] + 1, name=f"Restriccion12_4_{a}_{b}_{p}")

# 13. Asegurar que al menos un L% de los profesores con preferencia sean asignados a un auto que vaya a un bloque preferido
for b in B:
    model.addConstr(gp.quicksum(Za_b_p_r[a, b, p, r] * Fp_b[p, b] for a in A for p in P for r in R) >= L * gp.quicksum(Vp[p] for p in P), name=f"Restriccion13_{b}")

# 14. Cada auto solo puede ser activado si el auto anterior fue activado
for a in range(1, len(A)):
    model.addConstr(Xa[a] <= Xa[a-1], name=f"Restriccion14_{a}")

# Optimizar el modelo
model.optimize()

# Imprimir resultados
if model.status == GRB.OPTIMAL:
    print("Solución óptima encontrada.")
    # Imprimir o guardar los resultados en un archivo
else:
    print("No se encontró una solución óptima.")

# Guardar resultados en un archivo
results = []
for a in A:
    for p in P:
        for i in I:
            if Ta_p_i[a, p, i].X > 0.5:
                results.append((a, p, i, Ta_p_i[a, p, i].X))
df_results = pd.DataFrame(results, columns=["Auto", "Profesor", "Asiento", "Asignado"])
df_results.to_csv("resultados.csv", index=False)

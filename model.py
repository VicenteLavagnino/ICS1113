#----------------------- GUROBI ------------------------
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
from parameters import get_data


#----------------------- Generacion del modelo ------------------------

def generate_model(PARAMETERS):

    # Cargar datos desde parameters.py
    A, P, B, R, I, Ep1_p2, Jp_b, Dp_r, Fp_b, Mp, Qb_r, Vp, L = PARAMETERS

    for i in PARAMETERS:
        print(i)
    
    model = gp.Model("Fundacion_Atrevete")
    model.setParam("TimeLimit", 1800)  # Límite de tiempo de ejecución en 30 minutos

    #----------------------- Variables ------------------------
    Yp_r = model.addVars(P, R, vtype=GRB.BINARY, name="Yp_r")
    Ta_p_i = model.addVars(A, P, I, vtype=GRB.BINARY, name="Ta_p_i")
    Wa_b = model.addVars(A, B, vtype=GRB.BINARY, name="Wa_b")
    Za_b_p_r = model.addVars(A, B, P, R, vtype=GRB.BINARY, name="Za_b_p_r")
    Ha_p_i = model.addVars(A, P, I[:-1], vtype=GRB.BINARY, name="Ha_p_i")
    Sa_p1_p2_i = model.addVars(A, P, P, I[:-1], vtype=GRB.BINARY, name="Sa_p1_p2_i")
    Ua_b_p = model.addVars(A, B, P, vtype=GRB.BINARY, name="Ua_b_p")

    #----------------------- Funcion objetivo ------------------------
    model.setObjective(
    gp.quicksum(Sa_p1_p2_i[a, p1, p2, i] * Ep1_p2[(p1, p2)] for a in A for p1 in P for p2 in P for i in I[:-1] if (p1, p2) in Ep1_p2) +
    gp.quicksum(Ua_b_p[a, b, p] * Jp_b[(p, b)] for a in A for b in B for p in P if (p, b) in Jp_b),
    GRB.MINIMIZE)

    #----------------------- Restricciones ------------------------
    # 1. Cada auto tiene a lo más un profesor en cada asiento
    for a in A:
        for i in I:
            model.addConstr(gp.quicksum(Ta_p_i[a, p, i] for p in P) <= 1, name=f"Restriccion1_{a}_{i}")

    # 2. Cada auto es activado si y solo si tiene a algún profesor dentro. Este profesor debe ir en el asiento 0 (asiento del conductor)
    # y un auto está asociado a un bloque (y uno solo) si y solo si está activado
    for a in A:
        model.addConstr(gp.quicksum(Wa_b[a, b] for b in B) == gp.quicksum(Ta_p_i[a, p, 0] for p in P), name=f"Restriccion2_{a}")


    # 3. Cada auto solo puede tener a un profesor en el asiento i si hay un profesor en el asiento i-1
    for a in A:
        for i in range(1, 5):
            model.addConstr(gp.quicksum(Ta_p_i[a, p, i] for p in P) <= gp.quicksum(Ta_p_i[a, p, i-1] for p in P), name=f"Restriccion3_{a}_{i}")

    # 4. Si un profesor está en el asiento 0 de un auto, debe poder manejar
    for a in A:
        for p in P:
            model.addConstr(Ta_p_i[a, p, 0] <= Mp[p], name=f"Restriccion4_{a}_{p}")

    # 5. Cada profesor es asignado a un solo auto y a un solo asiento de este
    for p in P:
        model.addConstr(gp.quicksum(Ta_p_i[a, p, i] for a in A for i in I) <= 1, name=f"Restriccion5_{p}")

    # 6. A cada profesor se le asigna un solo ramo
    for p in P:
        model.addConstr(gp.quicksum(Yp_r[p, r] for r in R) <= 1, name=f"Restriccion6_{p}")

    # 7. El ramo al cual el profesor sea asignado debe ser uno de los ramos a los que postuló
    for p in P:
        for r in R:
            model.addConstr(Yp_r[p, r] <= Dp_r[p, r], name=f"Restriccion7_{p}_{r}")

    # 8. A cada bloque debe llegar la cantidad de profesores que se pidieron por ramo
    for a in A:
        for b in B:
            for p in P:
                for r in R:
                    model.addConstr(Za_b_p_r[a, b , p , r] <= gp.quicksum(Ta_p_i[a, p, i] for i in I), name=f"Restriccion8.1_{a}_{b}_{p}_{r}")
                    model.addConstr(Za_b_p_r[a, b , p , r] <= Wa_b[a, b], name=f"Restriccion8.2_{a}_{b}_{p}_{r}")
                    model.addConstr(Za_b_p_r[a, b , p , r] <= Yp_r[p, r], name=f"Restriccion8.3_{a}_{b}_{p}_{r}")
                    model.addConstr(Wa_b[a, b] + Yp_r[p, r] + gp.quicksum(Ta_p_i[a, p, i] for i in I) <= Za_b_p_r[a, b, p, r] + 2, name=f"Restriccion8.4_{a}_{b}_{p}_{r}")

    for b in B:
        for r in R:
            model.addConstr(gp.quicksum(Za_b_p_r[a, b, p, r] for a in A for p in P) == Qb_r[b, r], name=f"Restriccion8_{b}_{r}")

    # 9. Definición de la variable Sa_p1_p2_i
    for a in A:
        for p1 in P:
            for p2 in P:
                for i in range(0, 4):
                    model.addConstr(Sa_p1_p2_i[a, p1, p2, i] <= Ta_p_i[a, p1, i], name=f"Restriccion9.1_{a}_{p1}_{p2}_{i}")
                    model.addConstr(Sa_p1_p2_i[a, p1, p2, i] <= Ta_p_i[a, p2, i+1], name=f"Restriccion9.2_{a}_{p1}_{p2}_{i}")
                    model.addConstr(Ta_p_i[a, p1, i] + Ta_p_i[a, p2, i+1] <= 1 + Sa_p1_p2_i[a, p1, p2, i], name=f"Restriccion9.3_{a}_{p1}_{p2}_{i}")

    # 10. Definición de la variable Ha_p_i
    for a in A:
        for p in P:
            for i in range(0, 4):
                model.addConstr(Ha_p_i[a, p, i] <= Ta_p_i[a, p, i], name=f"Restriccion10.1_{a}_{p}_{i}")
                model.addConstr(Ha_p_i[a, p, i] <= 1 - gp.quicksum(Ta_p_i[a, p2, i+1] for p2 in P), name=f"Restriccion10.2_{a}_{p}_{i}")
                model.addConstr(Ta_p_i[a, p, i] - gp.quicksum(Ta_p_i[a, p2, i+1] for p2 in P) <= Ha_p_i[a, p, i], name=f"Restriccion10.3_{a}_{p}_{i}")

    # 11. Definición de la variable Ua_b_p
    for a in A:
        for b in B:
            for p in P:
                model.addConstr(Ua_b_p[a, b, p] <= Ta_p_i[a, p, 4] + gp.quicksum(Ha_p_i[a, p, i] for i in range(0, 4)), name=f"Restriccion11.1_{a}_{b}_{p}")
                model.addConstr(Ua_b_p[a, b, p] <= Wa_b[a, b], name=f"Restriccion11.2_{a}_{b}_{p}")
                model.addConstr(Wa_b[a, b] + Ta_p_i[a, p, 4] <= Ua_b_p[a, b, p] + 1, name=f"Restriccion11.3_{a}_{b}_{p}")
                model.addConstr(Wa_b[a, b] + gp.quicksum(Ha_p_i[a, p, i] for i in range(0, 4)) <= Ua_b_p[a, b, p] + 1, name=f"Restriccion11.4_{a}_{b}_{p}")

    # 12. Asegurar que al menos un L% de los profesores con preferencia sean asignados a un auto que vaya a un bloque preferido
    model.addConstr(gp.quicksum(Za_b_p_r[a, b, p, r] * Fp_b[p, b] for a in A for p in P for r in R for b in B) >= L * gp.quicksum(Vp[p] for p in P), name=f"Restriccion11_{b}")


    # Optimizar el modelo
    model.optimize()


    #----------------------- Solucion ------------------------
    # Verificar factibilidad del modelo y manejar la inviabilidad
    if model.status == GRB.INFEASIBLE:
        print("El modelo es inviable. Calculando IIS para diagnosticar...")
        model.computeIIS()
        model.write("model.ilp")  # Exportar el modelo a un archivo para análisis

        with open("infeasibility_report.txt", "w") as f:
            f.write("IIS Report:\n")
            for c in model.getConstrs():
                if c.IISConstr:
                    f.write(f"{c.constrName}\n")
    else:
        if model.status == GRB.OPTIMAL:
            print("Solución óptima encontrada.")
            # Guardar resultados en un archivo
            results = []
            for a in A:
                for p in P:
                    for i in I:
                        if Ta_p_i[a, p, i].X > 0.5:
                            results.append((a, p, i, Ta_p_i[a, p, i].X))
            df_results = pd.DataFrame(results, columns=["Auto", "Profesor", "Asiento", "Asignado"])
            df_results.to_csv("resultados.csv", index=False)
        else:
            print("No se encontró una solución óptima o el estado del modelo no es óptimo.")

    return model

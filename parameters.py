import pandas as pd

# MEDIANOS
e_profesor_profesor = pd.read_csv('source/medium/nuevo_E.csv', header=None)
j_profesor_bloque = pd.read_csv('source/medium/nuevo_J.csv', header=None)
postulaciones_profesores_ramos = pd.read_csv('source/medium/nuevo_D.csv', header=None)
preferencias_profesores_bloques = pd.read_csv('source/medium/nuevo_F.csv', header=None)
puede_manejar_profesores = pd.read_csv('source/medium/nuevo_M.csv', header=None)
q_profesor_ramo = pd.read_csv('source/medium/nuevo_Q.csv', header=None)

# PEQUEÑOS
#e_profesor_profesor = pd.read_csv('source/distancias_entre_profes.csv', header=None)
#j_profesor_bloque = pd.read_csv('source/distancias_profe_colegio.csv', header=None)
#postulaciones_profesores_ramos = pd.read_csv('source/ramos_postulados.csv', header=None)
#preferencias_profesores_bloques = pd.read_csv('source/preferencias_bloque.csv', header=None)
#puede_manejar_profesores = pd.read_csv('source/maneja.csv', header=None)
#q_profesor_ramo = pd.read_csv('source/requisitos_bloque.csv', header=None)


# GRANDES
#e_profesor_profesor = pd.read_csv('source/seeds/E-profesor-profesor.csv', header=0, index_col=0)
#j_profesor_bloque = pd.read_csv('source/seeds/J-profesor-bloque.csv', header=0, index_col=0)
#postulaciones_profesores_ramos = pd.read_csv('source/seeds/postulaciones_profesores_ramos.csv', header=0, index_col=0)
#preferencias_profesores_bloques = pd.read_csv('source/seeds/preferencias_profesores_bloques.csv', header=0, index_col=0)
#puede_manejar_profesores = pd.read_csv('source/seeds/puede_manejar_profesores.csv', header=0, index_col=0)
#q_profesor_ramo = pd.read_csv('source/seeds/Q-profesor-ramo.csv', header=0, index_col=0)

# Contar el número de profesores que pueden manejar
n_a = puede_manejar_profesores.sum()[0]

# Crear conjuntos
A = list(range(n_a))
P = list(range(len(j_profesor_bloque )))
B = list(range(len(j_profesor_bloque.columns)))
R = list(range(len(q_profesor_ramo.columns)))
I = [0, 1, 2, 3, 4]

# Crear parámetros
Ep1_p2 = {(i, j): int(e_profesor_profesor.iat[i, j]) for i in P for j in P}
Jp_b = {(i, j): int(j_profesor_bloque.iat[i, j]) for i in P for j in B}
Dp_r = {(i, j): int(postulaciones_profesores_ramos.iat[i, j]) for i in P for j in R}

Fp_b = {(i, j): int(preferencias_profesores_bloques.iat[i, j]) for i in P for j in B}
#Fp_b = {(i, j): 1 for i in P for j in B}
Mp = {i: int(puede_manejar_profesores.iat[i, 0]) for i in P}
Qb_r = {(i, j): int(q_profesor_ramo.iat[i, j]) for i in B for j in R}

# Tiene preferencia es ver si para cada profesor, tiene alguna preferencia (es tupla, es la suma)
Vp = {i: sum(Fp_b[(i, j)] for j in B) for i in P}

# Parámetro adicional
L = 1

# Exportar conjuntos y parámetros
def get_data():
    return A, P, B, R, I, Ep1_p2, Jp_b, Dp_r, Fp_b, Mp, Qb_r, Vp, L


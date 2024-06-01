import pandas as pd

# Leer datos desde archivos CSV (sin headers)
e_profesor_profesor = pd.read_csv('/mnt/data/E-profesor-profesor.csv', header=None)
j_profesor_bloque = pd.read_csv('/mnt/data/J-profesor-bloque.csv', header=None)
postulaciones_profesores_ramos = pd.read_csv('/mnt/data/postulaciones_profesores_ramos.csv', header=None)
preferencias_profesores_bloques = pd.read_csv('/mnt/data/preferencias_profesores_bloques.csv', header=None)
puede_manejar_profesores = pd.read_csv('/mnt/data/puede_manejar_profesores.csv', header=None)
q_profesor_ramo = pd.read_csv('/mnt/data/Q-profesor-ramo.csv', header=None)
tiene_preferencia_profesores = pd.read_csv('/mnt/data/tiene_preferencia_profesores.csv', header=None)

# Crear conjuntos
A = list(range(len(puede_manejar_profesores)))
P = list(range(len(j_profesor_bloque)))
B = list(range(len(j_profesor_bloque.columns)))
R = list(range(len(q_profesor_ramo.columns)))
I = [0, 1, 2, 3, 4]

# Crear parámetros
Ep1_p2 = {(i, j): e_profesor_profesor.iat[i, j] for i in P for j in P}
Jp_b = {(i, j): j_profesor_bloque.iat[i, j] for i in P for j in B}
Dp_r = {(i, j): postulaciones_profesores_ramos.iat[i, j] for i in P for j in R}
Fp_b = {(i, j): preferencias_profesores_bloques.iat[i, j] for i in P for j in B}
Mp = {i: puede_manejar_profesores.iat[i, 0] for i in P}
Qb_r = {(i, j): q_profesor_ramo.iat[i, j] for i in B for j in R}
Vp = {i: tiene_preferencia_profesores.iat[i, 0] for i in P}

# Parámetro adicional
L = 0.8

# Exportar conjuntos y parámetros
def get_data():
    return A, P, B, R, I, Ep1_p2, Jp_b, Dp_r, Fp_b, Mp, Qb_r, Vp, L
  

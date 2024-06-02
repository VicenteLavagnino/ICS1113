import pandas as pd

# Leer datos desde archivos CSV
e_profesor_profesor = pd.read_csv('source/seeds/E-profesor-profesor.csv', header=0, index_col=0)
j_profesor_bloque = pd.read_csv('source/seeds/J-profesor-bloque.csv', header=0, index_col=0)
postulaciones_profesores_ramos = pd.read_csv('source/seeds/postulaciones_profesores_ramos.csv', header=0, index_col=0)
preferencias_profesores_bloques = pd.read_csv('source/seeds/preferencias_profesores_bloques.csv', header=0, index_col=0)
puede_manejar_profesores = pd.read_csv('source/seeds/puede_manejar_profesores.csv', header=0, index_col=0)
q_profesor_ramo = pd.read_csv('source/seeds/Q-profesor-ramo.csv', header=0, index_col=0)
tiene_preferencia_profesores = pd.read_csv('source/seeds/tiene_preferencia_profesores.csv', header=0, index_col=0)

# Verificar que no haya valores NaN en los datos de entrada

print(e_profesor_profesor.isna().sum())
print(j_profesor_bloque.isna().sum())
print(postulaciones_profesores_ramos.isna().sum())
print(preferencias_profesores_bloques.isna().sum())
print(puede_manejar_profesores.isna().sum())
print(q_profesor_ramo.isna().sum())
print(tiene_preferencia_profesores.isna().sum())


# Rellenar NaN con un valor específico (e.g., 0)
e_profesor_profesor.fillna(0, inplace=True)
j_profesor_bloque.fillna(0, inplace=True)
postulaciones_profesores_ramos.fillna(0, inplace=True)
preferencias_profesores_bloques.fillna(0, inplace=True)
puede_manejar_profesores.fillna(0, inplace=True)
q_profesor_ramo.fillna(0, inplace=True)
tiene_preferencia_profesores.fillna(0, inplace=True)

# Crear conjuntos
A = list(range(len(puede_manejar_profesores)))
P = list(range(len(j_profesor_bloque)))
B = list(range(len(j_profesor_bloque.columns)))
R = list(range(len(q_profesor_ramo.columns)))
I = [0, 1, 2, 3, 4]

# Crear parámetros
Ep1_p2 = {(i, j): int(e_profesor_profesor.iat[i, j]) for i in P for j in P}
Jp_b = {(i, j): int(j_profesor_bloque.iat[i, j]) for i in P for j in B}
Dp_r = {(i, j): int(postulaciones_profesores_ramos.iat[i, j]) for i in P for j in R}
Fp_b = {(i, j): int(preferencias_profesores_bloques.iat[i, j]) for i in P for j in B}
Mp = {i: int(puede_manejar_profesores.iat[i, 0]) for i in P}
Qb_r = {(i, j): int(q_profesor_ramo.iat[i, j]) for i in B for j in R}
Vp = {i: int(tiene_preferencia_profesores.iat[i, 0]) for i in P}

# Parámetro adicional
L = 0.0

# Exportar conjuntos y parámetros
def get_data():
    return A, P, B, R, I, Ep1_p2, Jp_b, Dp_r, Fp_b, Mp, Qb_r, Vp, L

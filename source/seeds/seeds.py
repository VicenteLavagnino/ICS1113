import pandas as pd
import numpy as np

# Definiciones
ramos = ["Matemáticas", "Lenguaje", "Biología", "Física", "Química", "Historia"]
bloques = ["Bloque 1", "Bloque 2", "Bloque 3", "Bloque 4"]
n = 116  # Número de profesores
profesores = [f"Profesor {i+1}" for i in range(n)]


# ------ Q[b,r] ------

# Generar datos aleatorios para la cantidad de profesores necesarios
np.random.seed(0)  # Para reproducibilidad
datos = np.random.randint(1, 5, size=(len(bloques), len(ramos)))  # Entre 1 y 4 profesores por ramo y bloque

# Crear el DataFrame
df = pd.DataFrame(data=datos, index=bloques, columns=ramos)

# Generar el archivo CSV sin etiquetas de filas y columnas
df.to_csv("Q-profesor-ramo.csv", index=False, header=False)


# ------ J[p,b] ------

# Generar datos aleatorios para las distancias
np.random.seed(1)  # Para reproducibilidad
distancias = np.random.randint(5, 30, size=(len(profesores), len(bloques)))  # Distancias entre 5 y 30 km

# Crear el DataFrame
df_distancias = pd.DataFrame(data=distancias, index=profesores, columns=bloques)

# Generar el archivo CSV sin etiquetas de filas y columnas
df_distancias.to_csv("J-profesor-bloque.csv", index=False, header=False)


# ------ E[p1,p2] ------

# Crear una matriz inicial de ceros
distancias = np.zeros((n, n), dtype=int)

# Rellenar la matriz con valores aleatorios en la parte superior derecha
np.random.seed(2)  # Para reproducibilidad
for i in range(n):
    for j in range(i + 1, n):
        distancia = np.random.randint(1, 50)  # Distancias entre 1 y 49 km
        distancias[i, j] = distancia
        distancias[j, i] = distancia  # Asegura la simetría

# Crear el DataFrame
profesores = [f"Profesor {i+1}" for i in range(n)]
df_distancias = pd.DataFrame(data=distancias, index=profesores, columns=profesores)

# Generar el archivo CSV sin etiquetas de filas y columnas
df_distancias.to_csv("E-profesor-profesor.csv", index=False, header=False)


# ------ D[p,r] ------

# Generar datos aleatorios binarios para las postulaciones
np.random.seed(3)  # Para reproducibilidad
postulaciones = np.random.randint(0, 2, size=(n, len(ramos)))

# Crear el DataFrame
profesores = [f"Profesor {i+1}" for i in range(n)]
df_postulaciones = pd.DataFrame(data=postulaciones, index=profesores, columns=ramos)

# Generar el archivo CSV sin etiquetas de filas y columnas
df_postulaciones.to_csv("postulaciones_profesores_ramos.csv", index=False, header=False)


# ------ M[p] ------

# Generar datos aleatorios binarios para la capacidad de manejar
np.random.seed(4)  # Para reproducibilidad
puede_manejar = np.random.randint(0, 2, size=(n, 1))

# Crear el DataFrame
profesores = [f"Profesor {i+1}" for i in range(n)]
df_puede_manejar = pd.DataFrame(data=puede_manejar, index=profesores, columns=["Puede Manejar"])

# Generar el archivo CSV sin etiquetas de filas y columnas
df_puede_manejar.to_csv("puede_manejar_profesores.csv", index=False, header=False)


# ------ F[p, b] ------

# Generar datos aleatorios binarios para las preferencias de los bloques
np.random.seed(5)  # Para reproducibilidad
preferencias = np.random.randint(0, 2, size=(n, len(bloques)))

# Crear el DataFrame
profesores = [f"Profesor {i+1}" for i in range(n)]
df_preferencias = pd.DataFrame(data=preferencias, index=profesores, columns=bloques)

# Generar el archivo CSV sin etiquetas de filas y columnas
df_preferencias.to_csv("preferencias_profesores_bloques.csv", index=False, header=False)


print("Se han generado los archivos CSV necesarios para la semilla sin etiquetas de filas y columnas.")

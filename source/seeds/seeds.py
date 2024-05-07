import pandas as pd
import numpy as np


# ------ Q[b,r] ------

# Definir los ramos y los bloques
ramos = ["Matemáticas", "Lenguaje", "Biología", "Física", "Química", "Historia"]
bloques = ["Bloque 1", "Bloque 2", "Bloque 3", "Bloque 4"]

# Generar datos aleatorios para la cantidad de profesores necesarios
np.random.seed(0)  # Para reproducibilidad
datos = np.random.randint(1, 5, size=(len(bloques), len(ramos)))  # Entre 1 y 4 profesores por ramo y bloque

# Crear el DataFrame
df = pd.DataFrame(data=datos, index=bloques, columns=ramos)

# Generar el archivo CSV
df.to_csv("Q-profesor-ramo.csv", index=True)


# ------ J[p,b] ------

# Definir los profesores y los bloques
profesores = [f"Profesor {i+1}" for i in range(116)]
bloques = ["Bloque 1", "Bloque 2", "Bloque 3", "Bloque 4"]

# Generar datos aleatorios para las distancias
np.random.seed(1)  # Para reproducibilidad
distancias = np.random.randint(5, 30, size=(len(profesores), len(bloques)))  # Distancias entre 5 y 30 km

# Crear el DataFrame
df_distancias = pd.DataFrame(data=distancias, index=profesores, columns=bloques)

# Mostrar el DataFrame
print(df_distancias)

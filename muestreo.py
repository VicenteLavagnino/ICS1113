import random
from itertools import combinations

archivo_distancias_profes = open(
    "source/muestra_realista/distancias_entre_profesores.csv", "r")
distancias_pp = [l.strip("\n").split(",") for l in archivo_distancias_profes]
archivo_distancias_bloque = open(
    "source/muestra_realista/distancias_profesor_bloque.csv", "r")
distancias_pb = [l.strip("\n").split(",") for l in archivo_distancias_bloque]

# 16 profesores
muestra = random.sample(range(0, 104), 16)

# 4 colegios
colegios = [0, 1, 4, 5]

distancias_pp_muestra = [[0 for i in range(16)] for j in range(16)]
distancias_pb_muestra = [[0 for i in range(4)] for j in range(16)]

for i in range(16):
    for j in range(16):
        distancias_pp_muestra[i][j] = distancias_pp[muestra[i]][muestra[j]]

for i in range(16):
    for j in range(4):
        distancias_pb_muestra[i][j] = distancias_pb[muestra[i]][colegios[j]]

archivo_distancias_pp_nuevo = open(
    "source/muestreos/muestreo_5_16_profes/distancias_entre_profes.csv", "w")
for linea in distancias_pp_muestra:
    archivo_distancias_pp_nuevo.write(",".join(linea) + "\n")
archivo_distancias_pp_nuevo.close()

archivo_distancias_pb_nuevo = open(
    "source/muestreos/muestreo_5_16_profes/distancias_profe_colegio.csv", "w")
for linea in distancias_pb_muestra:
    archivo_distancias_pb_nuevo.write(",".join(linea) + "\n")
archivo_distancias_pb_nuevo.close()

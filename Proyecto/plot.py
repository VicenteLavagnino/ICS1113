import matplotlib.pyplot as plt
import numpy as np
import os
from time import sleep

def plot_solution():

    sleep(2) # Esperar a que se genere el archivo

    path = os.path.join(os.getcwd(), "output/resultado.txt")
    with open(path, 'r') as file:
        lineas = file.readlines()

    data = []

    for linea in lineas:
        
        if linea.startswith("El profesor"):
            div = linea.split()
            profesor = int(div[2])
            auto = int(div[7])
            asiento = int(div[11])
            bloque = int(div[17])
            clase = int(div[22].strip('.'))
            data.append((profesor, auto, asiento, bloque, clase))
        
        elif linea.startswith("Valor objetivo:"):
            objective_value = float(linea.split()[2])

        elif linea.startswith("Tiempo de ejecución:"):
            runtime = float(linea.split()[3])

        elif linea.startswith("Porcentaje mínimo de profesores asignados a bloques preferidos:"):
            L = float(linea.split()[8])



    # Crear el gráfico
    plt.figure(figsize=(10, 6))

    # Adaptar datos
    data_array = np.array(data)

    # Añadir nodos de profesores
    profesores = data_array[:, 0]
    plt.scatter(profesores, np.zeros_like(profesores), color='blue', label='Profesores')

    # Añadir nodos de autos
    autos = data_array[:, 1]
    plt.scatter(autos, np.ones_like(autos), color='green', label='Autos')

    # Añadir nodos de bloques
    bloques = data_array[:, 3]
    plt.scatter(bloques, 2 * np.ones_like(bloques), color='red', label='Bloques')

    # Dibujar arcos entre los nodos
    for profesor, auto, asiento, bloque, clase in data:
        plt.plot([profesor, auto], [0, 1], 'k-', lw=0.5)
        plt.plot([auto, bloque], [1, 2], 'k-', lw=0.5)

    # Añadir etiquetas y título
    plt.xlabel('ID')
    plt.ylabel('Tipo de nodo')
    plt.yticks([0, 1, 2], ['Profesores', 'Autos', 'Bloques'])
    plt.title(f'Visualización \nValor objetivo: {objective_value}')
    plt.subplots_adjust(bottom=0.2)
    plt.figtext(0.5, 0.05, f'Tiempo de ejecución: {runtime} segundos\nPorcentaje mínimo de profesores asignados a bloques preferidos: {L}', ha="center", fontsize=10)
    plt.legend()
    plt.grid(True)
    plt.show()

    return None

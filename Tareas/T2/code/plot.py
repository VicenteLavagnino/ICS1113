# TAREA 2 [JACINTA ORTIZ Y VICENTE LAVAGNINO]

# Pregunta 1
import matplotlib.pyplot as plt
import numpy as np

# RANGOS
x1 = np.linspace(-10, 10, 1000)
x2_r1 = (9 - x1) / 3
x2_r2 = 4 - 2 * x1
x2_r3 = 1 - x1
x2_r4 = 0
x1_r5 = 0

# EJES Y RECTAS
plt.figure(figsize=(8, 6))

plt.plot(x1, x2_r1, label='$x_1 + 3x_2 \leq 9$')
plt.plot(x1, x2_r2, label='$2x_1 + x_2 \leq 4$')
plt.plot(x1, x2_r3, label='$x_1 + x_2 \geq 1$')
plt.plot(x1, x2_r4 * np.ones_like(x1), label='$x_2 \geq 0$')
plt.plot(x1_r5 * np.ones_like(x1), x1, label='$x_1 \geq 0$')

# VECTOR GRADIENTE
plt.quiver(0, 0, 1, 1, angles='xy', scale_units='xy', scale=1, color='Black', label=' Vector Gradiente')

# LEYENDAS
plt.legend()
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.title('Visualización Pregunta 1')
plt.xlim(0, 5)
plt.ylim(0, 5)

# #VERTICES
vertices = [(0.6, 2.8), (2, 0), (1, 0), (0, 1), (0, 3) ]
infactibles = [(0,0), (3, -2), (0,4), (9,0)]

# PUNTOS
for i, vertice in enumerate(vertices):
    plt.plot(vertice[0], vertice[1], 'ro')
    plt.text(vertice[0], vertice[1] + 0.05, f'$VF_{i+1}$', fontsize=10)

for i, infactible in enumerate(infactibles):
    plt.plot(infactible[0], infactible[1], 'ro')
    plt.text(infactible[0], infactible[1] + 0.05, f'$VI_{i+1}$', fontsize=10)


# VISUALIZAR
plt.show()

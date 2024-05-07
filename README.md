# Proyecto ICS113 [Grupo 31]

Repositorio del Grupo 31 para el curso Optimización ICS1113 2024-1 

## Integrantes
- Sebastián Silva
- Sebastián Plaza
- Felipe Eskenazi
- Jacinta Ortiz
- Vicente Lavagnino


## Descripción

Este proyecto desarrolla un modelo de optimización para mejorar la eficiencia del traslado de profesores voluntarios en la Fundación Atrevete, una entidad educacional sin fines de lucro que ofrece un preuniversitario a estudiantes destacados de colegios vulnerables en Santiago de Chile. El principal objetivo del proyecto es minimizar los costos y tiempos de traslado, optimizando la asignación de profesores a colegios y coordinando sus desplazamientos en grupo para reducir tanto el impacto ambiental como los recursos financieros empleados.

### Contexto

La Fundación Atrevete enfrenta el desafío de asignar eficientemente a sus 116 profesores voluntarios a cinco colegios, teniendo en cuenta la ubicación de los colegios y las preferencias y capacidades de los profesores. Actualmente, la asignación se realiza manualmente usando formularios de Google, lo que puede ser ineficiente y propenso a errores.

### Objetivos del Modelo

El modelo de optimización busca diseñar una logística de traslado que:
- Minimice la distancia total recorrida por los autos, reduciendo así los costos operativos y el tiempo de traslado.
- Asegure la asignación correcta de profesores a los ramos que pueden dictar, en función de sus postulaciones.
- Mantenga la consistencia y la calidad de la enseñanza, asegurando que cada bloque de clases reciba el número adecuado de profesores especializados requeridos.

La implementación de este modelo no solo mejora la operación logística de la fundación, sino que también contribuye a la sostenibilidad financiera y organizacional de la entidad, permitiendo una mayor expansión de sus programas educativos y mejorando la infraestructura para el beneficio de más estudiantes.


## Se asume que:

- Se tiene instalado gurobi y se cuenta con la licensia correspondiente.
- Se usa Python 3.12.2 o posteriores



## Configuración del entorno

Para instalar todas las dependencias necesarias, incluyendo Gurobi y cualquier otro paquete de Python necesario, ejecuta el siguiente comando en tu terminal:

```bash
pip3 install -r requirements.txt
```

## Ejecución

Ubicándonos en la raíz de nuestro directorio

```bash
python3 main.py
```

## Estructura del código

/proyecto
│
├── main.py         # Script principal que ejecuta el modelo de optimización.
├── model.py        # Script donde se instancia el modelo de optimización.
├── parameters.py   # Script donde se instancian los parametros necesarios para el modelo.
├── helpers.py      # Scripts auxiliares con funciones adicionales.
│
├── source/
│   └── datos.csv   # Datos necesarios para ejecutar el modelo.
│
├── output/
│   └── AAAAA.csv   # AAAAA
│
├── requirements.txt     # Dependencias del proyecto.
└── README.md            # Documentación del proyecto.





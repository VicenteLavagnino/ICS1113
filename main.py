# PROYECTO FINAL - GRUPO 31

# IMPORTAR
from parameters import get_data
from model import generate_model
from plot import plot_solution


if __name__ == '__main__':

    # PREGUNTAR QUE BBDD QUIERE USAR

    print("          WELCOME TO THE FUNDACION ATREVETE PROJECT          ")
    print("-------------------------------------------------------------")
    print("          CHOOSE THE DATABASE THAT YOU WANT TO USE           ")
    print("                                                             ")
    print("WE HAVE 4 DATABASES: seeds, small, medium, big or real. CHOOSE ONE")

    print("-------------------------------------------------------------")
    print("                           HINT                              ")
    print(" A MOTIVOS DE CORRECCION, SE RECOMIENDA USAR small o medium  ")
    print("-------------------------------------------------------------")

    BBDD = input("Write the DB that you want to use: ")

    if BBDD == "seeds":
        parameters = get_data("seeds")

    elif BBDD == "small":
        parameters = get_data("small")

    elif BBDD == "medium":
        parameters = get_data("medium")

    elif BBDD == "big":
        parameters = get_data("big")

    elif BBDD == "real":
        parameters = get_data("real")

    else:
        print("                   ERROR: DATABASE NOT FOUND                 ")
        print("-------------------------------------------------------------")
        exit()

    # GENERAR EL MODELO
    generate_model(parameters)
    

import pandas as pd


def get_data(csv_type):

    if csv_type == "seeds":

        # SEEDS
        e_profesor_profesor = pd.read_csv(
            'source/seeds/E-profesor-profesor.csv', header=None)
        j_profesor_bloque = pd.read_csv(
            'source/seeds/J-profesor-bloque.csv', header=None)
        postulaciones_profesores_ramos = pd.read_csv(
            'source/seeds/postulaciones_profesores_ramos.csv', header=None)
        preferencias_profesores_bloques = pd.read_csv(
            'source/seeds/preferencias_profesores_bloques.csv', header=None)
        puede_manejar_profesores = pd.read_csv(
            'source/seeds/puede_manejar_profesores.csv', header=None)
        q_profesor_ramo = pd.read_csv(
            'source/seeds/Q-profesor-ramo.csv', header=None)

    elif csv_type == "small":

        # PEQUEÑOS
        e_profesor_profesor = pd.read_csv(
            'source/small/distancias_entre_profes.csv', header=None)
        j_profesor_bloque = pd.read_csv(
            'source/small/distancias_profe_colegio.csv', header=None)
        postulaciones_profesores_ramos = pd.read_csv(
            'source/small/ramos_postulados.csv', header=None)
        preferencias_profesores_bloques = pd.read_csv(
            'source/small/preferencias_bloque.csv', header=None)
        puede_manejar_profesores = pd.read_csv(
            'source/small/maneja.csv', header=None)
        q_profesor_ramo = pd.read_csv(
            'source/small/requisitos_bloque.csv', header=None)

    elif csv_type == "medium":

        # MEDIANOS
        e_profesor_profesor = pd.read_csv(
            'source/medium/nuevo_E.csv', header=None)
        j_profesor_bloque = pd.read_csv(
            'source/medium/nuevo_J.csv', header=None)
        postulaciones_profesores_ramos = pd.read_csv(
            'source/medium/nuevo_D.csv', header=None)
        preferencias_profesores_bloques = pd.read_csv(
            'source/medium/nuevo_F.csv', header=None)
        puede_manejar_profesores = pd.read_csv(
            'source/medium/nuevo_M.csv', header=None)
        q_profesor_ramo = pd.read_csv('source/medium/nuevo_Q.csv', header=None)

    elif csv_type == "big":

        # MEDIANOS
        e_profesor_profesor = pd.read_csv(
            'source/big/nuevo_E.csv', header=None)
        j_profesor_bloque = pd.read_csv('source/big/nuevo_J.csv', header=None)
        postulaciones_profesores_ramos = pd.read_csv(
            'source/big/nuevo_D.csv', header=None)
        preferencias_profesores_bloques = pd.read_csv(
            'source/big/nuevo_F.csv', header=None)
        puede_manejar_profesores = pd.read_csv(
            'source/big/nuevo_M.csv', header=None)
        q_profesor_ramo = pd.read_csv('source/big/nuevo_Q.csv', header=None)

    # COMPARTIDO -----------------------

    # Contar el número de profesores que pueden manejar
    n_a = puede_manejar_profesores.sum()[0]

    # Crear conjuntos
    A = list(range(n_a))
    P = list(range(len(j_profesor_bloque)))
    B = list(range(len(j_profesor_bloque.columns)))
    R = list(range(len(q_profesor_ramo.columns)))
    I = [0, 1, 2, 3, 4]

    # Crear parámetros
    Ep1_p2 = {(i, j): int(e_profesor_profesor.iat[i, j]) for i in P for j in P}
    Jp_b = {(i, j): int(j_profesor_bloque.iat[i, j]) for i in P for j in B}
    Dp_r = {(i, j): int(
        postulaciones_profesores_ramos.iat[i, j]) for i in P for j in R}
    Fp_b = {(i, j): int(
        preferencias_profesores_bloques.iat[i, j]) for i in P for j in B}
    Mp = {i: int(puede_manejar_profesores.iat[i, 0]) for i in P}
    Qb_r = {(i, j): int(q_profesor_ramo.iat[i, j]) for i in B for j in R}

    # Tiene preferencia es ver si para cada profesor tiene alguna preferencia (1 si tiene, 0 si no)
    Vp = {i: 1 if sum(Fp_b[(i, j)] for j in B) > 0 else 0 for i in P}

    # Parámetro adicional
    
    L = float(input("Ingrese el porcentaje minímo de los profesores que serán asignados a alguno de sus bloques preferios, este valor debe estar entre 0 y 1: "))

    if L < 0 or L > 1 or type(L) != float:
        print("El valor ingresado no es válido")
        exit()

    # Exporta los conjuntos
    return A, P, B, R, I, Ep1_p2, Jp_b, Dp_r, Fp_b, Mp, Qb_r, Vp, L

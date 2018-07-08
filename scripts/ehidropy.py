#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


def make_matrix(data, function):
    """
    Crea una matriz de n vs n variables como un dataframe
    :param data: Diccionario que contiene el nombre de la variable (key) y
    los valores a procesar (value)
    :param function: Funcion que establece el tipo de operacion a realizar
    para la generacion de la martriz
    :return: Data frame
    """
    cols = [i for i in data]
    cols.sort()
    matrix = {col: [function(data[i], data[col]) for i in cols] for col in cols}
    return pd.DataFrame(matrix, cols)


def make_matrix_radio_correlative(**kwargs):
    """
    Construir la matriz para el calculo del radio correlativo, para esto es
    necesario el uso de las matrices de correlacion, gradiente y diferencias
    absolutas.
    :param kwargs: Se debe especificar el key de la variable con cada matriz
    es decir:
        make_matrix_radio_correlative(matrix_co= value, matrix_gr=value, matrix_da=value)
    :return: Data frame con la matriz configurada
    ejemplo:
             matrix_co matrix_gr  matrix_si
        0     0.980166  4.832349  0.026490
        1     0.814514  2.320805  0.227008
        2     0.858036  1.487427  0.177911
        3     0.223214  3.046485  0.640877

    """
    dcc = dict()
    for k, mx in kwargs.items():
        tmp = [v.tolist()[index:] for index, (i, v) in enumerate(mx.iterrows(), 1)]
        dcc[k] = [y for x in tmp for y in x]
    matrix = pd.DataFrame(dcc)
    return matrix
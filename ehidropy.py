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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _karasiev import *
from ehidropy import *
from longcor import *

# Variables globales
BUDYKO_FIELD = 'BDK'
ID_FIELD = 'HYBAS_ID'
CODCUENCA = 'IDRC'
EPSG = 32718
YEARS_OF_READER = 20

# Probando la clase Karasiev de _karasiev
ksv = Karasiev()
ksv.set_epsg(EPSG)

# Se obtiene el codigo de las cuencas
# cuencas = set([i[0] for i in arcpy.da.SearchCursor(EHIDROMETRICA, [CODCUENCA], "%s IN ('004984918')" % CODCUENCA)])
cuencas = set([i[0] for i in arcpy.da.SearchCursor(EHIDROMETRICA, [CODCUENCA], "%s IS NOT NULL" % CODCUENCA)])
cuencas = ['000131804']


for i in cuencas:
    print i
    ksv.set_filter(cuenca=i)

    # Generar matrices
    data_mx_absolute_difference = ksv.get_data_mx_absolute_difference(ID_FIELD, BUDYKO_FIELD)
    matrix_da = make_matrix(data_mx_absolute_difference, ksv.mx_absolute_difference)  # ehidropy

    data_mx_distance = ksv.get_data_mx_distance(ID_FIELD, 'SHAPE@')
    matrix_di = make_matrix(data_mx_distance, ksv.mx_distance)  # ehidropy

    matrix_gr = ksv.mx_gradient(matrix_da, matrix_di)
    matrix_co = ksv.mx_correlation(matrix_gr)
    matrix_si = ksv.mx_significance(matrix_co, YEARS_OF_READER)

    # Crear carpeta
    pathMatrix = os.path.join(MATRIX_DIR, i)
    if not os.path.exists(pathMatrix):
        os.makedirs(pathMatrix)

    # Expotando matrices como archivos *.csv
    matrix_da.to_csv(os.path.join(pathMatrix, 'matrix_da_%s.csv' % i))
    matrix_di.to_csv(os.path.join(pathMatrix, 'matrix_di_%s.csv' % i))
    matrix_gr.to_csv(os.path.join(pathMatrix, 'matrix_gr_%s.csv' % i))
    matrix_co.to_csv(os.path.join(pathMatrix, 'matrix_co_%s.csv' % i))
    matrix_si.to_csv(os.path.join(pathMatrix, 'matrix_si_%s.csv' % i))

    # Probando la generacion de la matrices de radio correlativo (lo)
    matrix_rc = make_matrix_radio_correlative(mx_gr=matrix_gr, mx_di=matrix_di, mx_co=matrix_co, mx_si=matrix_si)
    matrix_rc.to_csv(os.path.join(pathMatrix, 'matrix_rc_%s.csv' % i))

    # Realizar los graficos
    get_idrc(i)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _karasiev import *
from ehidropy import *

# Variables globales
BUDYKO_FIELD = 'Q_Budyko'
ID_FIELD = 'HYBAS_ID'
EPSG = 32717
YEARS_OF_READER = 20

# Probando la clase Karasiev de _karasiev
ksv = Karasiev()
ksv.set_epsg(EPSG)

# Generar matrices
data_mx_absolute_difference = ksv.get_data_mx_absolute_difference(ID_FIELD, BUDYKO_FIELD)
matrix_da = make_matrix(data_mx_absolute_difference, ksv.mx_absolute_difference)  # ehidropy

data_mx_distance = ksv.get_data_mx_distance(ID_FIELD, 'SHAPE@')
matrix_di = make_matrix(data_mx_distance, ksv.mx_distance)  # ehidropy

matrix_gr = ksv.mx_gradient(matrix_da, matrix_di)
matrix_co = ksv.mx_correlation(matrix_gr)
matrix_si = ksv.mx_significance(matrix_co, YEARS_OF_READER)

# Expotando matrices como archivos *.csv
matrix_da.to_csv(os.path.join(MATRIX_DIR, 'matrix_da.csv'))
matrix_di.to_csv(os.path.join(MATRIX_DIR, 'matrix_di.csv'))
matrix_gr.to_csv(os.path.join(MATRIX_DIR, 'matrix_gr.csv'))
matrix_co.to_csv(os.path.join(MATRIX_DIR, 'matrix_co.csv'))
matrix_si.to_csv(os.path.join(MATRIX_DIR, 'matrix_si.csv'))

# Probando la generacion de la matrices de radio correlativo (lo)
matrix_rc = make_matrix_radio_correlative(mx_gr=matrix_gr, mx_co=matrix_co, mx_si=matrix_da)  # ehidropy
matrix_rc.to_csv(os.path.join(MATRIX_DIR, 'matrix_rc.csv'))

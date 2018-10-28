#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from _karasiev import *
from ehidropy import *
from longcor import *

# Variables globales
BUDYKO_FIELD = 'q_bdk'
ID_FIELD = 'HYBAS_ID'
CODCUENCA = 'IDRC'
EPSG = 32718

YEARS_OF_READER = 20
# ERROR_SIST = [0.10, 0.15, 0.20]  # Error sistematico
ERROR_SIST = [0.20]  # Error sistematico

# Probando la clase Karasiev de _karasiev
ksv = Karasiev()
ksv.set_epsg(EPSG)

# Se obtiene el codigo de las cuencas
cuencas = set([i[0] for i in arcpy.da.SearchCursor(EHIDROMETRICA, [CODCUENCA], "%s IS NOT NULL" % CODCUENCA)])
cuencas = list(cuencas)

# cuencas = ["000013207P", "000499313A", "004987705A"]

s_container=[]

for i in cuencas:
    try:
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

        # Graficos
        lo = get_idrc(i)

        runoff = [v for k, v in data_mx_absolute_difference.items()]
        longrio = [m[0] for m in arcpy.da.SearchCursor(TB_IDRC, ["LONG_RIO"], "%s = '%s'" %(CODCUENCA, i))][0]

        # Graficos
        row = dict()
        container = []
        for es in ERROR_SIST:
            row["idcr"] = i
            row["lo"]= lo                           # Distancia entre centroides
            row["yo"] = np.mean(runoff)             # Norma de escorrentia
            row["std"] = np.std(runoff)             # Desviacion estandar
            row["cv"] = row["std"]/row["yo"]        # Covarianza
            row["o"] = es                           # Error sistematico
            row["a"] = 1/row["lo"]                  # a
            row["gyo"] = matrix_gr.unstack().mean() # Gradiente promedio
            row["lrio"] = longrio                   # Longitud de rio
            row["lgrad"] = (2*pow(2, 0.5)*es*row["yo"])/row["gyo"]   # Longitud de gradiente
            row["lcor"] = pow(es, 2)/(row["a"]*pow(row["cv"], 2))    # Longitud correlativa
            row["lopt"] = (row["lgrad"]+row["lcor"])/2               # Longitud optima
            row["eopt"] = round(row["lrio"]/row["lopt"], 0)                    # Numero optimo de estaciones

            a = dict(row)
            container.append(a)
            s_container.append(a)

        df = pd.DataFrame.from_dict(container)
        df.to_csv(os.path.join(pathMatrix, 'eoptimas_%s.csv' % i), index=False)

    except Exception as e:
        print e.message

sdf = pd.DataFrame.from_dict(s_container)
sdf.to_csv(os.path.join(MATRIX_DIR, 'estaciones_optimas.csv'), index=False)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import numpy as np
from _karaziev_criterios import *
from make_matrix import *
from _karaziev_longcor import *

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

# cuencas = ["001371208P", "000498105A"]

s_container=[]

for i in cuencas:
    try:
        print i

        ksv.set_filter(cuenca=i)
        len_ehidro = len([x[0] for x in arcpy.da.SearchCursor(EHIDROMETRICA, [ID_FIELD], ksv.get_filter)])

        row = dict()
        container = []

        if len_ehidro < 5:
            for es in ERROR_SIST:
                rowsX = [x[0] for x in arcpy.da.SearchCursor(EHIDROMETRICA, ["SHAPE@X"], ksv.get_filter)]
                rowsY = [x[0] for x in arcpy.da.SearchCursor(EHIDROMETRICA, ["SHAPE@Y"], ksv.get_filter)]
                runoff = [x[0] for x in arcpy.da.SearchCursor(EHIDROMETRICA, [BUDYKO_FIELD], ksv.get_filter)]
                lo = np.sqrt(pow(max(rowsX) - min(rowsX), 2) + pow(max(rowsY) - min(rowsY), 2))
                longrio = [m[0] for m in arcpy.da.SearchCursor(TB_IDRC, ["LONG_RIO"], "%s = '%s'" % (CODCUENCA, i))][0]

                row["idcr"] = i
                row["lo"] = lo  # Distancia entre centroides
                row["yo"] = np.mean(runoff)  # Norma de escorrentia
                row["std"] = np.std(runoff)  # Desviacion estandar
                row["cv"] = row["std"] / row["yo"]  # Covarianza
                row["o"] = es  # Error sistematico
                row["a"] = 1 / row["lo"]  # a
                row["gyo"] = "0"
                row["lrio"] = longrio  # Longitud de rio
                row["lgrad"] = row["lrio"] / len_ehidro  # Longitud de gradiente
                row["lcor"] = "0"  # Longitud correlativa
                row["lopt"] = (np.mean(runoff)/np.sum(runoff))*longrio   # Longitud optima
                row["eopt"] = round(row["lrio"] / row["lopt"], 0)  # Numero optimo de estaciones

                row["flagLo"] = "0"

                a = dict(row)
                container.append(a)
                s_container.append(a)

        else:

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
            if lo[1] == 1:
                flagLo = "Distancia"
            elif lo[1] == 2:
                flagLo = "Gradiente"
            else:
                flagLo = "Sin interseccion"

            runoff = [v for k, v in data_mx_absolute_difference.items()]
            longrio = [m[0] for m in arcpy.da.SearchCursor(TB_IDRC, ["LONG_RIO"], "%s = '%s'" %(CODCUENCA, i))][0]

            # Graficos

            for es in ERROR_SIST:
                row["idcr"] = i
                if lo[1]==3:
                    rowsX = [x[0] for x in arcpy.da.SearchCursor(EHIDROMETRICA, ["SHAPE@X"], ksv.get_filter)]
                    rowsY = [x[0] for x in arcpy.da.SearchCursor(EHIDROMETRICA, ["SHAPE@Y"], ksv.get_filter)]
                    runoff = [x[0] for x in arcpy.da.SearchCursor(EHIDROMETRICA, [BUDYKO_FIELD], ksv.get_filter)]
                    lo_N = np.sqrt(pow(max(rowsX) - min(rowsX), 2) + pow(max(rowsY) - min(rowsY), 2))
                    row["lo"] = lo_N / len_ehidro
                else:
                    row["lo"] = lo[0]                   # Distancia entre centroides
                row["yo"] = np.mean(runoff)             # Norma de escorrentia
                row["std"] = np.std(runoff)             # Desviacion estandar
                row["cv"] = row["std"]/row["yo"]        # Covarianza
                row["o"] = es                           # Error sistematico
                row["a"] = 1/row["lo"]                  # a
                row["gyo"] = matrix_gr.unstack().mean() # Gradiente promedio
                row["lrio"] = longrio                   # Longitud de rio
                row["lgrad"] = (2*pow(2, 0.5)*es*row["yo"])/row["gyo"]   # Longitud de gradiente

                lcor = pow(es, 2) / (row["a"] * pow(row["cv"], 2))
                row["lcor"] = pow(es, 2)/(row["a"]*pow(row["cv"], 2))    # Longitud correlativa
                if row["lo"] > row["lrio"]:
                    row["lopt"] = row["lgrad"]
                else:
                    row["lopt"] = (row["lgrad"]+row["lcor"])/2               # Longitud optima
                row["eopt"] = round(row["lrio"]/row["lopt"], 0)          # Numero optimo de estaciones

                row["flagLo"] = flagLo                  # Distancia: intersec Dist, Gradiente: Normal

                a = dict(row)
                container.append(a)
                s_container.append(a)

        df = pd.DataFrame.from_dict(container)
        df.to_csv(os.path.join(pathMatrix, 'eoptimas_%s.csv' % i), index=False)

    except:
        traceback.print_exc()

sdf = pd.DataFrame.from_dict(s_container)
sdf.to_csv(os.path.join(MATRIX_DIR, 'estaciones_optimas.csv'), index=False)
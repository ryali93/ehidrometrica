from config import *
import arcpy
from itertools import combinations
import numpy as np
import pandas as pd

ehidrometricas = EHIDROMETRICA

_L_OPT = "L_OPT"         # Longitud optima definida por la metodologia de Karasiev
_IDRC = "IDRC"           # Identificador de las region-cuenca
_EHIDROID = "EHIDROID"   # Identificador de cada estacion hidrometrica

loptima = pd.read_csv('estaciones_optimas.csv')

_LOPT = 'lopt'
_IDCR = 'idcr'

def get_longitud_optima(idrc):
    response = loptima[loptima[_IDCR]==idrc][_LOPT]
    return response.iloc[0]

all_idrc = list(set([i[0] for i in arcpy.da.SearchCursor(ehidrometricas, [_IDRC])]))

aceptados = list()
result = list()
longitud_optima = float()
primer_filtro = list()
factor = 1

def evaluador(*args):
    """
    Determina aquellas estaciones hidrometricas de un IDRC que se encuentran
    separadas a una mayor o igual distancia_optima
    """
    global longitud_optima
    global factor
    a, b = args[0]
    d = a[-1].distanceTo(b[-1]) / 1000
    if d >= longitud_optima * factor:
        return [a[0], b[0], d]
    else:
        return False

def buscar_optimos(*args):
    """
    Determina todas las soluciones posibles de agrupacion entre estaciones hidrometricas
    que se encuentran separadas a una mayor o igual distancia_optima
    """
    global aceptados
    global longitud_optima
    global primer_filtro
    ini, fin, dist = args
    for n in filter(lambda x: sorted(x) != sorted(list(args)), primer_filtro):
        if fin in n:
            ini_tmp = n[1] if n.index(fin) else n[0]
            fin_tmp = n[0] if n.index(fin) else n[1]
            if fin_tmp in list(set([q for x in aceptados for q in x[:2]])):
                continue
            dist_tmp = n[-1]
            controlador = 1
            for p in list(set([q for x in aceptados for q in x[:2]])):
                val = [l for l in primer_filtro if p in l and fin_tmp in l]
                if not val:
                    controlador = 0
                    break
            if controlador:
                aceptados.append(n)
                buscar_optimos(ini_tmp, fin_tmp, dist_tmp)  # recursividad

def get_estaciones_optimas(idrc):
    """
    Realiza la evaluacion de un IDRC para determinar la mejor solucion
    """
    try:
        global result
        global longitud_optima
        global soluciones
        global primer_filtro
        global aceptados
        print('Evaluando: {}'.format(idrc))

        query = "{} = '{}'".format(_IDRC, idrc)
        src = arcpy.SpatialReference(32718)
        geom = [i for i in arcpy.da.SearchCursor(ehidrometricas, [_EHIDROID, "SHAPE@", _L_OPT], query, src)]
        longitud_optima = get_longitud_optima(idrc)

        geom = map(lambda x: (x[0], x[1]), geom)

        combinaciones = list(combinations(geom, 2))

        primer_filtro = filter(lambda i: i, map(evaluador, combinaciones))

        for i in primer_filtro:
            ini, fin, dist = i
            aceptados.append(i)
            buscar_optimos(ini, fin, dist)
            soluciones.append(aceptados[:])
            aceptados = list()

        # Se obtiene la desviacion estandar de cada solucion en una lista, junto al index
        std_distancia = map(lambda i: [soluciones.index(i), np.std(map(lambda x: x[-1], i))], soluciones)

        # Se ordena de menor a mayor en base a la desviacion estandar
        std_distancia.sort(key=lambda i: i[-1], reverse=False)

        # Se obtiene el primer valor como solucion del proceso, ya que esto significa que la distancia
        # entre estaciones es la mas homogene
        solucion = soluciones[std_distancia[0][0]]

        # Se extraen los EHIDROID que pertenecen al index seleccionado
        optimos_list = list(set([q for x in solucion for q in x[:2]]))

        for i in optimos_list:
            result.append({_EHIDROID: i, 'OPT': 1})

        return {_IDRC: idrc, 'msg': 'success'}
    except Exception as e:
        return {_IDRC: idrc, 'msg': e.message.__str__()}
    finally:
        primer_filtro = list()
        soluciones = list()

logs = map(get_estaciones_optimas, all_idrc)

df_optimos = pd.DataFrame(result)
df_optimos.to_excel('estaciones_hidrometricas_optimas.xls')

df_logs = pd.DataFrame(logs)
df_logs.to_excel('logs.xls')
result= list()
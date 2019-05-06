# coding=utf-8
# -*- codign: utf-8 -*-

"""
C8 se han seguido los siguientes pasos:
A partir de la cobertura de comisarías a nivel nacional se han realizado diferentes áreas de influencia cada uno con un peso respectivo como a continuacion:

C8:
1:  5 Km
2: 10 Km
3: 15 Km
4: 20 Km

C11 se han seguido los siguientes pasos:
Se ha recogido información de diferentes fuentes para establecer cuales son los principales usuarios que requieren la ubicacion de estaciones hidrologicas.
Una vez ubicados, se les ha realizado un area de influencia con pesos acumulativos en las intersecciones, los pesos asignados se muestran a continuacion. 

C11:
1: (a) Conservación de peces y víveres
2: (b) Comercial
3: (c) Poblacional
4: (d) Agricola
4: (e) Potencia termoeléctrica
4: (f) Industrial
4: (g) Navegación
"""
import arcpy
from config import *

arcpy.env.overwriteOutput = True

def criterio8():
    pass

def criterio11_first():
    gdb = os.path.join(STATIC, 'users.gdb')
    arcpy.env.workspace = gdb
    scratch = arcpy.env.scratchGDB
    listFeature = arcpy.ListFeatureClasses()
    print listFeature

    for i in listFeature:
        print i
        buff = arcpy.GraphicBuffer_analysis(i, os.path.join(scratch, i), "{} Kilometers".format(i[1]), "ROUND", "ROUND")
        diss = arcpy.Dissolve_management(buff, os.path.join(scratch, "diss_{}".format(i)), '#', '#', 'MULTI_PART', 'DISSOLVE_LINES')
        ft = arcpy.AddField_management(diss, "C11", "TEXT", '#', '#',10)
        with arcpy.da.UpdateCursor(ft, "C11") as cursor:
            for x in cursor:
                x[0] = i[1]
                cursor.updateRow(x)


def criterio11_second():
    gdb = os.path.join(STATIC, 'usersdissolve.gdb')
    arcpy.env.workspace = gdb
    scratch = arcpy.env.scratchGDB
    listFeature = arcpy.ListFeatureClasses()

    union = arcpy.Union_analysis(listFeature, os.path.join(scratch, "C11_union"), 'ALL', '#', 'GAPS')
    ft = arcpy.AddField_management(union, "C11_PND", "TEXT", '#', '#',10)
    listFields = [x.name for x in arcpy.ListFields(ft) if x.name[0:3] == "C11"]

    with arcpy.da.UpdateCursor("C11_union", listFields) as cursor:
        for x in cursor:
            suma = 0
            l = x[0:-1]
            for y in l:
                if y != "":
                    suma = suma + int(y)
            x[-1] = suma
            cursor.updateRow(x)

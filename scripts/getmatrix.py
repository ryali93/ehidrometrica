#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Estimacion de matrices usando los criterios de Karasiev
"""

# from _karasiev import *
#
#
# def _get_data_ehidrometricas():
#     res = {i[0]: i[1] for i in arcpy.da.SearchCursor(
#         EHIDROMETRICA_NA, ['OID@', 'SHAPE@']
#     )}
#     return res
#
#
# data = _get_data_ehidrometricas()
# print data

from settings import *
from osgeo import ogr
import arcpy
from datetime import datetime

print 'OSGEO'
start_osgeo = datetime.now()
shp = ogr.Open(EHIDROMETRICA_NA)
lyr = shp.GetLayer()
# fields = [field.name for field in lyr.schema]
rows_osgeo = {i.GetFID(): i.GetGeometryRef() for i in lyr}
print datetime.now() - start_osgeo
# for i in lyr:
#     print dir(i)
#     break

print 'ARCPY'
start_arcpy = datetime.now()
# print arcpy.GetCount_management(EHIDROMETRICA).__str__()
rows_arcpy = {i[0]: i[1] for i in arcpy.da.SearchCursor(EHIDROMETRICA_NA, ['OID@', 'SHAPE@'])}
print datetime.now() - start_arcpy

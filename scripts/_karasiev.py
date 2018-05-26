#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
from settings import *


def matrix_dabsoluta():
    pass


# # @matrix_distance
# def _append_data(code_cuenca):
#     arcpy.management.DeleteRows()
#     sql = "CODIGO = '%s'" % code_cuenca
#     mfl = arcpy.management.MakeFeatureLayer(EHIDROMETRICA, 'Mfl', sql)
#     arcpy.management.Append()


def matrix_distance(geom_x, geom_y):
    analyst_type = arcpy.MakeRouteLayer_na(
        REDHIDRICA_NA, 'Route', 'Length', 'USE_INPUT_ORDER', 'PRESERVE_BOTH',
        'NO_TIMEWINDOWS', '#', 'ALLOW_UTURNS', 'Oneway', 'NO_HIERARCHY', '#', 'TRUE_LINES_WITH_MEASURES', '#'
    )

    arcpy.AddLocations_na(analyst_type, 'Stops', geom_x,
                          'Name OBJECTID #', '5000 Meters', '#', 'redhidrica SHAPE;redhidrica_ND_Junctions NONE',
                          'MATCH_TO_CLOSEST', 'APPEND', 'NO_SNAP', '5 Meters', 'INCLUDE',
                          'redhidrica #;redhidrica_ND_Junctions #'
                          )

    arcpy.AddLocations_na(analyst_type, 'Stops', geom_y,
                          'Name OBJECTID #', '5000 Meters', '#', 'redhidrica SHAPE;redhidrica_ND_Junctions NONE',
                          'MATCH_TO_CLOSEST', 'APPEND', 'NO_SNAP', '5 Meters', 'INCLUDE',
                          'redhidrica #;redhidrica_ND_Junctions #'
                          )

    arcpy.Solve_na(analyst_type)


def matrix_gradient():
    pass


def matrix_correlation():
    pass


def matrix_significance():
    pass

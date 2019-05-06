# coding=utf-8
# -*- codign: utf-8 -*-

"""
C1 y C2 se han seguido los siguientes pasos:
Analisis de redes de cada estacion hidrometrica al centro poblado mas cercano, donde se
extrae la distancia y tipo de via, determinando un tiempo aproximado (C1) y un ponderado
del acceso a la estacion (C2):

C1:
1: > 5 Horas 0 - 0.25
2: < 5 Horas y > 3 Horas 0.25 - 0.50
3: < 3 Horas y > 1.5 Horas 0.50 - 0.75
4: < 1.5 Horas 0.75 - 1

C2:
1: Herradura (4 Km/h)
2: Carrozable o Fluvial ( Km/h)
3: Afirmada ( Km/h)
4: Asfaltada (70 Km/h)
"""
from __future__ import print_function

import sys
import arcpy
import arcpy.na as na
import traceback
import pandas as pd
from config import *

arcpy.env.overwriteOutput = True

_TRACK_NA = os.path.join(STATIC, r'response.gdb\NAEHidro\NAEHidro_ND')
_TRACK_SHP = os.path.join(STATIC, r'response.gdb\NAEHidro\GPL_Tracks')
_INCIDENTS = os.path.join(STATIC, 'response.gdb\GPT_EHidrometrica')
_FACILITIES = os.path.join(STATIC, r'response.gdb\GPT_CcppUrbano')
_TARGET_SHP = os.path.join(STATIC, r'response.gdb\GPL_TrackByEHidrometrica')
_OUT_CSV = os.path.join(STATIC, 'criterioaccesibilidad.csv')
_CODCCPP = 'CODCCPP'
_HYBASID = 'EHIDROID'
_SUPVIA = 'SUP_VIA'
_HIERARCHY = 'HIERARCHY'
_TOLERANCE = '5000 Meters'
_BUUFER_DISTANCE = '1 Meters'


def get_parameters(ini=None, end=None):
    parameters = [i[0] for i in arcpy.da.SearchCursor(_INCIDENTS, [_HYBASID])]
    return parameters[ini:end]


def define_analyst():
    network_tmp = na.MakeClosestFacilityLayer(_TRACK_NA, 'Closest Facility',
                                              'Length', 'TRAVEL_TO', '#',
                                              '1', 'Length', 'ALLOW_UTURNS',
                                              '#', 'NO_HIERARCHY', '#',
                                              'TRUE_LINES_WITH_MEASURES', '#')  # .getOutput(0)
    return network_tmp


def update_facilities():
    na.AddLocations(network, 'Facilities', _FACILITIES,
                    'Name {} #'.format(_CODCCPP), _TOLERANCE, '#',
                    'tracks SHAPE;tracks_ND_Junctions NONE',
                    'MATCH_TO_CLOSEST', 'APPEND', 'NO_SNAP',
                    '5 Meters', 'INCLUDE', 'tracks #;tracks_ND_Junctions #')
    # return facilities


def update_incidents(mlayer):
    arcpy.DeleteRows_management('Closest Facility\Incidents')
    arcpy.AddLocations_na(network, 'Incidents', mlayer, 'Name {} #'.format(_HYBASID),
                          _TOLERANCE, '#', 'tracks SHAPE;tracks_ND_Junctions NONE',
                          'MATCH_TO_CLOSEST', 'APPEND', 'NO_SNAP', '5 Meters', 'INCLUDE',
                          'tracks #;tracks_ND_Junctions #')
    # return incidents


def execute_analyst(hybasid):
    response_tmp = dict()
    response_tmp[_HYBASID] = hybasid
    try:
        print('NA: {}'.format(hybasid))
        query = "{} = '{}'".format(_HYBASID, hybasid)
        name = 'analystnetworkmfl'
        flayer = arcpy.MakeFeatureLayer_management(_INCIDENTS, name, query)
        update_incidents(flayer)
        na.Solve(network)

        buff = arcpy.Buffer_analysis('Closest Facility\Routes', 'in_memory\\a{}'.format(name), _BUUFER_DISTANCE)
        clip = arcpy.Clip_analysis(_TRACK_SHP, buff, 'in_memory\\b{}'.format(name))

        with arcpy.da.UpdateCursor(clip, [_HYBASID]) as cursor:
            for row in cursor:
                row[0] = hybasid
                cursor.updateRow(row)
            del cursor

        with arcpy.da.UpdateCursor(_TARGET_SHP, [_HYBASID], query) as cursor:
            for row in cursor:
                cursor.deleteRow()
            del cursor

        case = ';'.join([_SUPVIA, _HIERARCHY, _HYBASID])
        diss = arcpy.Dissolve_management(clip, 'in_memory\d{}'.format(name), case, '#', 'MULTI_PART', 'DISSOLVE_LINES')

        arcpy.Append_management(diss, _TARGET_SHP, 'NO_TEST')

        arcpy.DeleteRows_management('Closest Facility\Routes')

        response_tmp['state'] = 1
        response_tmp['msg'] = 'success'
    except Exception as e:
        print(e.message.__str__())
        response_tmp['state'] = 0
        msg = traceback.format_exc().__str__()
        msg = msg.replace(',', ' ')
        msg = msg.replace('\n', ' ')
        response_tmp['msg'] = msg
    return response_tmp


if __name__ == '__main__':
    network = define_analyst()
    update_facilities()
    params = sys.argv[1].split(',')
    response = [execute_analyst(i) for i in params]
    df = pd.DataFrame(response)
    df.to_csv(_OUT_CSV)

# -*- coding: utf-8 -*-

import arcpy

arcpy.env.overwriteOutput = True

_factor = 0.3

cuencas = r'D:\DANELROCK_PC\devs\ehidrometrica\static\ehidrometrica.gdb\EH_GPO_Cuenca'
_codigo = 'CODIGO'  # Codigo de la cuenca

redHidrica = r'D:\DANELROCK_PC\devs\ehidrometrica\static\ehidrometrica.gdb\EH_GPL_RedHidrica'
_codcuenca = 'CODCUENCA'  # Codigo de la cuenca
_rprin = 'RPRIN'  # Rio principal
_gridcode = 'GRID_CODE'  # Orden de rio

shp_cuencas = {i[0]: i[-1] for i in arcpy.da.SearchCursor(cuencas, [_codigo, 'SHAPE@'])}
rhLayer = arcpy.MakeFeatureLayer_management(redHidrica, 'mfl')  # Feature layer de la ref hidrica (redHidrica)


def determinar_rio_principal(codigo, shape):
    """
    
    :param codigo:
    :param shape:
    :return:
    """
    arcpy.SelectLayerByLocation_management(rhLayer, "INTERSECT", shape, "#", "NEW_SELECTION")
    with arcpy.da.UpdateCursor(rhLayer, [_codcuenca]) as cursor:
        for i in cursor:
            i[0] = codigo
            cursor.updateRow(i)
        del cursor
    orden_tmp = [i[0] for i in
                 arcpy.da.SearchCursor(rhLayer, [_gridcode], None, None, False, (None, 'GROUP BY %s' % _gridcode))]
    arcpy.CalculateField_management(rhLayer, _codcuenca, codigo)
    n = int(round(len(orden_tmp) * _factor))
    assert n != 0, 'Cuenca no evaluable...'
    orden_tmp.sort(reverse=True)
    orden = ', '.join(map(lambda x: str(x), orden_tmp[:n]))
    arcpy.SelectLayerByAttribute_management(rhLayer, 'NEW_SELECTION',
                                            "%s IN (%s) AND %s = '%s'" % (_gridcode, orden, _codcuenca, codigo))
    arcpy.CalculateField_management(rhLayer, _rprin, 1)
    arcpy.SelectLayerByAttribute_management(rhLayer, 'CLEAR_SELECTION')


for k, v in shp_cuencas.items():
    try:
        print k
        determinar_rio_principal(k, v)
    except Exception as e:
        print e.message

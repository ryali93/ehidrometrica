import os
import arcpy
import shapefile
import traceback
from config.settings import *

arcpy.env.overwriteOutput = True

ORDEN_RIOS = os.path.join(STATIC, 'ehidrometrica.gdb\\EH_GPL_RedHidrica')
CUENCAS = r'D:\SENAMHI\ehidrometrica\test\EH_GPO_HYDROHSED12.shp'
OUTPUT = r'D:\SENAMHI\ehidrometrica\test\EH_Base3.shp'
OUTPUT_GDB = r'D:\SENAMHI\ehidrometrica\ehidrometrica\static\ehidrometrica.gdb\EH_GPT_Base_Titicaca'

ORDEN_RIOS = arcpy.Intersect_analysis([ORDEN_RIOS, CUENCAS], 'in_memory\\rios', 'ALL', '#', 'INPUT')
rows = list()

class ShapeBUILD(object):
    def __init__(self):
        self.shp = shapefile.Writer(shapefile.POINT)
        self.shp.field('HYBAS_ID', 'N', decimal=0)

    def register(self, **kwargs):
        self.shp.record(kwargs.get('id'))
        self.shp.point(kwargs.get('coords')[0], kwargs.get('coords')[1])

    def save(self):
        self.shp.save(OUTPUT)


def get_points(data):
    dss = arcpy.Dissolve_management(data, 'in_memory\dissolve')
    coords = [[i[0].lastPoint.X, i[0].lastPoint.Y] for i in
              arcpy.da.SearchCursor(dss, ["SHAPE@"], None, arcpy.SpatialReference(32718))][0]
    return coords

try:
    shp = ShapeBUILD()

    if os.path.exists(CUENCAS):
        cuencas_rows = [[x[0], x[1]] for x in arcpy.da.SearchCursor(CUENCAS, ["HYBAS_ID", "SHAPE@"])]
    else:
        raise RuntimeError('No existe el feature de cuencas')

    orden_rios_mfl = arcpy.management.MakeFeatureLayer(ORDEN_RIOS, 'orden_rios')

    for i, x in enumerate(cuencas_rows, 1):
        print i, int(x[0])
        arcpy.management.SelectLayerByLocation(orden_rios_mfl, "WITHIN", x[1], "#", "NEW_SELECTION")
        r = [i[0] for i in arcpy.da.SearchCursor(orden_rios_mfl, ["grid_code"])]
        if len(r) > 0:
            mx = max(r)
            if mx:
                rios = [i[0] for i in arcpy.da.SearchCursor(orden_rios_mfl, ["SHAPE@"], "grid_code = %s" % mx)]
                pnt = get_points(rios)
                if pnt:
                    shp.register(id=x[0], coords=pnt)
    shp.save()
    # arcpy.env.outputCoordinateSystem = 4326
    arcpy.CopyFeatures_management(OUTPUT, OUTPUT_GDB)
except:
    print traceback.format_exc()

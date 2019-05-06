#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
import pandas as pd
from config import *

arcpy.env.overwriteOutput = True

TB_EHOPT = os.path.join(MATRIX_DIR, 'TB_IDRC.csv')
EHYDRO = EHIDROMETRICA
DF = pd.read_csv(TB_EHOPT, sep=";")
DF = DF[['IDRC', 'L_OPT', 'EH_OPT']]
scratch = arcpy.env.scratchFolder

class assignEopt(object):
    def assignEopt_1(self):
        for k, v in DF.iterrows():
            sql = "IDRC = '{}'".format(v[0])
            order = (None, "order by MCA desc")
            print sql
            counter = 0
            with arcpy.da.UpdateCursor(EHYDRO, ["EHIDROID", "MCA", "E_OPT_V1", "L_OPT"], sql, None, False, order) as cursor:
                for x in cursor:
                    counter += 1
                    if counter > v[2]:
                        break
                    x[2] = 1
                    x[3] = v[1]
                    cursor.updateRow(x)

            if "L_OPT_M" in [x.name for x in arcpy.ListFields(EHYDRO)]:
                arcpy.AddField_management(EHYDRO, "L_OPT_M", "DOUBLE")

    def assignEopt_2(self):
        arcpy.CalculateField_management(EHYDRO, "L_OPT_M", "!L_OPT!*1000", "PYTHON_9.3")
        self.buffer = arcpy.Buffer_analysis(EHYDRO, os.path.join(scratch, "bufferTmp"), "L_OPT_M", "FULL", "ROUND", "NONE", "#", "PLANAR")
        for k, v in DF.iterrows():
            sql = "IDRC = '{}'".format(v[0])
            self.bufferMfl = arcpy.MakeFeatureLayer_management(self.buffer, "mfl", sql)
            lenBuffer = int(arcpy.GetCount_management(self.bufferMfl).getOutput(0))
            print sql + "    Count: " + str(lenBuffer)

    def selectBestRing(self, rings, sql):
        if rings < 4:
            eh = arcpy.MakeFeatureLayer_management(EHYDRO, "eh", sql)
            arcpy.SelectLayerByLocation_management(self.bufferMfl, 'INTERSECT', eh, '#', 'NEW_SELECTION', 'NOT_INVERT')
            arcpy.SelectLayerByAttribute_management(self.bufferMfl, "CLEAR_SELECTION")

    def main(self):
        # self.assignEopt_1()
        self.assignEopt_2()

# if __name__ == '__main__':
#     poo = assignEopt()
#     poo.main()
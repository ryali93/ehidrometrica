#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

__author__ = 'GEOCODERY'
__copyright__ = 'GEOCODERY 2018'
__credits__ = ['Daniel Aguado H.', 'Roy Yali S.']
__version__ = '1.0.1'
__maintainer__ = ['Daniel Aguado H.', 'Roy Yali S.']
__mail__ = 'geocodery@gmail.com'
__status__ = 'Development'

BASE_DIR = os.path.dirname(__file__)    # Directorio principal del proyecto

STATIC = os.path.join(BASE_DIR, "static")
IMG = os.path.join(STATIC, "img")
SHP = os.path.join(STATIC, "shp")

TEMP = os.path.join(BASE_DIR, "temp")   # Directorio de archivos intermedios


# IMG_FILE = {
#     "ASP": os.path.join(IMG, "BD_ASP.tif"),
#     "DEM": os.path.join(IMG, "BD_DEM.tif"),
#     "FAC": os.path.join(IMG, "BD_FAC.tif"),
#     "FDR": os.path.join(IMG, "BD_FDR.tif"),
#     "GLC": os.path.join(IMG, "BD_GLC.tif"),
#     "PPM": os.path.join(IMG, "BD_PPM.tif"),
#     "RUS": os.path.join(IMG, "BD_RUS.tif"),
#     "SLP": os.path.join(IMG, "BD_SLP.tif"),
#     "TWI": os.path.join(IMG, "BD_TWI.tif")
# }

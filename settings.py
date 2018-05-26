#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# Metadata
__author__ = 'GEOCODERY'
__copyright__ = 'GEOCODERY 2018'
__credits__ = ['Daniel Aguado H.', 'Roy Yali S.']
__version__ = '1.0.1'
__maintainer__ = ['Daniel Aguado H.', 'Roy Yali S.']
__mail__ = 'geocodery@gmail.com'
__status__ = 'Development'

# Directorio principal del proyecto
BASE_DIR = os.path.dirname(__file__)

# Directorio ue sirve de archivos estaticos
STATIC = os.path.join(BASE_DIR, "static")

IMG = os.path.join(STATIC, "img")

# Diretorio de archivos shapefile
SHP = os.path.join(STATIC, "shp")
EHIDROMETRICA = os.path.join(SHP, 'EH_01.shp')
REDHIDRICA = os.path.join(SHP, 'OrdenRios.shp')

# Directorio de archivos shapefile para el analisis de redes
NETWORK_DIR = os.path.join(STATIC, 'network')
EHIDROMETRICA_NA = os.path.join(NETWORK_DIR, 'ehidrometrica.shp')
REDHIDRICA_NA = os.path.join(NETWORK_DIR, 'redhidrica.shp')
NETWORK = os.path.join(NETWORK_DIR, 'redhidrica_ND')  # Red de analisis

# Directorio de archivos temporales
TEMP = os.path.join(BASE_DIR, "temp")

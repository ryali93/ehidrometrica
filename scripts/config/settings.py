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
BASE_DIR = os.path.abspath(os.path.join(__file__, '..\..\..'))

# Directorio ue sirve de archivos estaticos
STATIC = os.path.join(BASE_DIR, "static")

# IMG = os.path.join(STATIC, "img")
MATRIX_DIR = os.path.join(STATIC, 'matrix')

# Tabla de longitud de rios
TB_IDRC = os.path.join(STATIC, 'ehidrometrica.gdb\\tb_idrc')

# Geodatabase
EHIDROMETRICA = os.path.join(STATIC, 'ehidrometrica.gdb\\EH_GPT_EstacionHidrometrica')

# # Directorio de archivos temporales
# TEMP = os.path.join(BASE_DIR, "temp")

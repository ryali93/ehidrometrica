#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
from config.settings import *

_CODCUENCA = 'IDRC'
_CODREGION = 'CODREGION'   # Nombre de campo identificador de region aun no definido


class Karasiev(object):
    """
    Karasiev: ...
    """
    __epsg = int()
    __query = None

    def set_epsg(self, value):
        """
        Establece el sistema de referencia para realizar el procesamiento
        :param value: codigo epsg
        :return: asigna el valor ingresado a la variable self.__epsg
        """
        self.__epsg = value

    @property
    def get_epsg(self):
        """
        Muestra el codigo epsg configurado
        :return: self.__epsg
        """
        return self.__epsg

    def set_filter(self, **kwargs):
        """
        Permite realizar el filtro por cuenca, region, o ambos
        :param kwargs:
        :return:
        """
        query = [None] * 2

        query[0] = "%s = '%s'" % (_CODREGION, kwargs['region']) if kwargs.get('region') else None
        query[1] = "%s = '%s'" % (_CODCUENCA, kwargs['cuenca']) if kwargs.get('cuenca') else None

        query = filter(lambda i: i is not None, query)

        if query:
            self.__query = ' AND '.join(query)
        else:
            raise RuntimeError('Invalid values...')

    @property
    def get_filter(self):
        return self.__query

    def mx_absolute_difference(self, x, y):
        """
        Muestra la diferencia absoluta entre los elementos
        :param x: Primer valor
        :param y: Segundo valor
        :return: Diferencia absoluta
        """
        return abs(x - y)

    def mx_distance(self, x, y):
        """
        Calcula la distancia entre las estaciones hidrometricas en
        kilometros (km.)
        :param x: Objeto geometria shape@ de la primera estacion hidrometrica
        :param y: Objeto geometria shape@ de la segunda estacion hidrometrica
        :return: Distancia
        """
        val = x.distanceTo(y) / 1000
        return val

    def mx_gradient(self, mx_da, mx_di):
        """
        Diferencia absoluta entre parejas de estaciones sobre la distancia entre estaciones
        :param mx_da: Matriz de diferencia absoluta entre parejas de estaciones
        :param mx_di: Matriz de distancias entre estaciones
        :return: Matriz de Gradiente
        """
        return mx_da / mx_di

    def mx_correlation(self, x):
        """
        Muestra la correlación de una matriz
        :param x: Matriz de gradiente
        :return: Matriz de correlaciones
        """
        # print x.corr()
        return x.corr()

    def mx_significance(self, mx_co, n_years):
        """
        Permite crear la matriz de significancia
        :param matCor: Matriz de correlacion
        :param lenData: Cantidad de datos en las estaciones
        :return: matriz de significancia
        """
        return 1.5 * 1.96 * (1 - (mx_co * mx_co)) / (n_years - 1) ** 0.5

    def correlative_radio(self):
        """
        Distancia a partir de la cual se pierde la correlacion entre estaciones
        :return:
        """
        pass

    def get_data_mx_absolute_difference(self, *args):
        """
        Obtiene el caudal anual de cada estacion hidrometrica
        :param args: [campo identificador, campo caudal]
        :return: caudal anual como dict()
        """
        if not self.__query:
            raise RuntimeError('self.query is not configured...')

        data = {str(int(x[0])): x[1] for x in arcpy.da.SearchCursor(EHIDROMETRICA, args, self.__query)}
        return data

    def get_data_mx_distance(self, *args):
        """
        Obtiene la posicion de cada estacion hidrometrica
        :param args: [campo identificador, campo geometria]
        :return: posicion como dict()
        """
        if not self.__query:
            raise RuntimeError('self.query is not configured...')

        data = {str(int(i[0])): i[1] for i in
                arcpy.da.SearchCursor(EHIDROMETRICA, args, self.__query, arcpy.SpatialReference(self.__epsg))}
        return data

    def __str__(self):
        res = {
            'estacion_hidrometrica': EHIDROMETRICA,
            'epsg': self.__epsg
        }
        return res

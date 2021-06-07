"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros


def init():
    catalogo = model.newCatalog()
    return catalogo

# Funciones para la carga de datos


def loadConnections(catalog, connectionsFile):
    cFile = cf.data_dir + connectionsFile
    input_file = csv.DictReader(open(cFile, encoding="utf-8"),
                                delimiter=",")

    for connection in input_file:
        model.addConnection(catalog, connection)

    return catalog


def loadCountries(catalog, countriesFile):
    cFile = cf.data_dir + countriesFile
    input_file = csv.DictReader(open(cFile, encoding="utf-8"),
                                delimiter=",")
    size = len(input_file)
    i = 0
    last_country = 0
    for country in input_file:
        if i == (size-1):
            last_country = country

        model.addCountry(catalog, country)
        i += 1

    return catalog, last_country


def loadLp(catalog, LpFile):
    cFile = cf.data_dir + LpFile
    input_file = csv.DictReader(open(cFile, encoding="utf-8"),
                                delimiter=",")
    i = 0
    primer_lp = 0
    for lp in input_file:
        if i == 0:
            primer_lp = lp

        model.addLp(catalog, lp)
        i += 1
    return catalog, primer_lp

# Funciones de consulta

def totalVertex(catalog):
    return model.totalVertex(catalog)


def totalConnections(catalog):
    return model.totalConnections(catalog)


def totalCountries(catalog):
    return model.totalCountries(catalog)


def getClusters(catalog, lp1, lp2):
    return model.getClusters(catalog, lp1, lp2)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

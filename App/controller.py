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
    connectionsFile = cf.data_dir + connectionsFile
    input_file = csv.DictReader(open(connectionsFile, encoding="utf-8"),
                                delimiter=",")
    lastConnection = None
    for connection in input_file:
        if lastConnection is not None:
            sameConnection = lastConnection['cable_id'] == connection['cable_id']
            sameStop = lastConnection['destination'] == connection['destination']
            if sameConnection and not sameStop:
                model.addStopConnection(catalog, lastConnection, connection)
        lastConnection = connection
    model.addRouteConnections(catalog)

    return catalog


def loadCountries(catalog, countriesFile):
    countriesFile = cf.data_dir + countriesFile
    input_file = csv.DictReader(open(countriesFile, encoding="utf-8"),
                                delimiter=",")
    for country in input_file:
        model.addCountry(catalog, country)
    return catalog


def loadLp(catalog, LpFile):
    LpFile = cf.data_dir + LpFile
    input_file = csv.DictReader(open(LpFile, encoding="utf-8"),
                                delimiter=",")
    for lp in input_file:
        model.addLp(catalog, lp)
    return catalog

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

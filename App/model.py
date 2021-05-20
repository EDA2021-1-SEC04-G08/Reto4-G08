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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from re import split
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog = {'stops': None,
               'connections': None,
               'components': None,
               'paths': None,
               'countries': None,
               'landing_points': None}
    
    catalog['stops'] = mp.newMap(numelements= 3300,
                                 maptype='PROBING',
                                 comparefunction=compareLd)

    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                         directed=True,
                                         size=3300,
                                         comparefunction=compareLd)
    
    catalog['countries'] = lt.newList('ARRAY_LIST')
    catalog['landing_points'] = lt.newList('ARRAY_LIST')

    return catalog


# Funciones para agregar informacion al catalogo


def addStopConnection(catalog, lastConnection, connection):
    origin = formatVertex(lastConnection)
    destination = formatVertex(connection)
    cleanConnectionDistance(connection)
    distance = connection['cable_length']
    addStop(catalog, origin)
    addStop(catalog, destination)
    addConnection(catalog, origin, destination, distance)
    addRouteStop(catalog, connection)
    addRouteStop(catalog, lastConnection)
    return catalog


def addStop(catalog, stopid):
    if not gr.containsVertex(catalog['connections'], stopid):
        gr.insertVertex(catalog['connections'], stopid)
    return catalog


def addRouteStop(catalog, connection):
    entry = mp.get(catalog['stops'], connection['destination'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, connection['cable_id'])
        mp.put(catalog['stops'], connection['destination'], lstroutes)
    else:
        lstroutes = entry['value']
        info = connection['cable_id']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return catalog


def addRouteConnections(catalog):
    lststops = mp.keySet(catalog['stops'])
    for key in lt.iterator(lststops):
        lstroutes = mp.get(catalog['stops'], key)['value']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(catalog, prevrout, route, 0)
                addConnection(catalog, route, prevrout, 0)
            prevrout = route


def addConnection(catalog, origin, destination, distance):
    edge = gr.getEdge(catalog['connections'], origin, destination)
    if edge is None:
        gr.addEdge(catalog['connections'], origin, destination, distance)
    return catalog


def addCountry(catalog, country):
    lt.addLast(catalog['countries'], country)
    return catalog


def addLp(catalog, lp):
    lt.addLast(catalog['landing_points'], lp)
    return catalog

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista


def compareLd(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

# Funciones de ordenamiento
# Funciones helper

def formatVertex(connection):
    name = connection['destination'] + '-'
    name = name + connection['cable_id']
    return name


def cleanConnectionDistance(connection):
    d1 = connection['cable_length']
    d2 = d1.split(' ')
    d3 = d2[0].split(',')
    if len(d3) > 1:
        d4 = d3[0] + d3[1]
    else:
        d4 = d3[0]
    connection['cable_length'] = d4


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


from os import name
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from math import *
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog = {'connections': None,
               'countries_con': None,
               'countries': None,
               'landing_points': None}
    
    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                         directed=True,
                                         size=14000,
                                         comparefunction=compareLd)

    catalog['countries_con'] = mp.newMap(numelements= 14000,
                                         maptype='PROBING',
                                         comparefunction=compareroutes)
    
    catalog['countries'] = mp.newMap(numelements= 14000,
                                     maptype='PROBING',
                                     comparefunction=compareroutes)
        
    catalog['landing_points'] = mp.newMap(numelements= 14000,
                                          maptype='PROBING',
                                          comparefunction=compareroutes)

    return catalog

# Funciones para agregar informacion al catalogo


def addConnection(catalog, connection):
    cable_name = connection['cable_name']
    origin = formatVertex(catalog, connection['origin'], cable_name)
    destination = formatVertex(catalog, connection['destination'], cable_name)
    distance = getConnectionDistance(catalog, connection)
    addLp(catalog, origin)
    addLp(catalog, destination)
    addArco(catalog, origin, destination, distance)
    capacity = float(connection['capacityTBPS'])
    connection_name = origin + ', ' + destination + ', ' + cable_name
    addCapitalLp(catalog, connection, destination, connection_name, capacity)
    return catalog


def addLp(catalog, stopid):
    if not gr.containsVertex(catalog['connections'], stopid):
        gr.insertVertex(catalog['connections'], stopid)
    return catalog


def addArco(catalog, origin, destination, distance):
    edge = gr.getEdge(catalog['connections'], origin, destination)
    if edge is None:
        gr.addEdge(catalog['connections'], origin, destination, distance)
    return catalog


def addCountry(catalog, country):
    mp.put(catalog['countries'], country['CountryName'].lower(), country)
    return catalog


def addLp(catalog, lp):
    mp.put(catalog['landing_points'],int(lp['landing_point_id']), lp)
    return catalog


def addCapitalLp(catalog, connection, destination, connection_name, capacity):
    lp = mp.get(catalog['landing_points'], int(connection['destination']))
    entry = me.getValue(lp)
    name = entry['name'].split(', ')
    name_size = len(name)

    if name_size == 3:
        country = name[2].lower()
    elif name_size == 2:
        country = name[1].lower()
    else:
        country = 'None'

    if mp.contains(catalog['countries_con'], country):
        info = mp.get(catalog['countries_con'], country)
        lista = me.getValue(info)
 
    else:
        lista = lt.newList('ARRAY_LIST')
    lt.addLast(lista, {'name':connection_name, 'capacityTBPS':capacity, 'destination':destination})

    getCapital = mp.get(catalog['countries'], country)
    entry2 = me.getValue(getCapital)
    capital = [country, entry2['CapitalName']]
    addLp(catalog['connections'], capital)

    min = 1000000

    for con in lt.iterator(lista):
        if con['capacity'] < min:
            min = con['capacity']

    for con in lt.iterator(lista):
        if con['destination'] != destination:
            addArco(catalog, destination, con['destination'], 0.1)
            
    addArco(catalog, destination, capital, min)
    mp.put(catalog['countries_con'], country, lista)
    
    return catalog

# Funciones para creacion de datos

# Funciones de consulta


def totalVertex(catalog):
    return gr.numVertices(catalog['connections'])


def totalConnections(catalog):
    return gr.numEdges(catalog['connections'])


def totalCountries(catalog):
    return mp.size(catalog['countries'])


def getClusters(catalog, lp1, lp2):
    clusters = scc.KosarajuSCC(catalog['connections'])
    num_clusters = scc.connectedComponents(clusters)
    is_conected = scc.stronglyConnected(clusters, lp1, lp2)

    return (num_clusters, is_conected)

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

def formatVertex(catalog, connection, cable_name):
    lp = mp.get(catalog['landing_points'], int(connection))
    entry = me.getValue(lp)
    name = entry['id'] + '-'
    name = name + cable_name
    return name


def getConnectionDistance(catalog, connection):
    origin = connection['origin']
    lp = mp.get(catalog['landing_points'], int(origin))
    entry = me.getValue(lp)
    lat1 = float(entry['latitude'])
    lon1 = float(entry['longitude'])

    destination = connection['destination']
    lp = mp.get(catalog['landing_points'], int(destination))
    entry2 = me.getValue(lp)
    lat2 = float(entry2['latitude'])
    lon2 = float(entry2['longitude'])

    distance = funcionHaversine(lat1, lat2, lon1, lon2)

    return distance

def funcionHaversine(lat1, lat2, lon1, lon2):
    difLat = lat2 - lat1
    difLon = lon2 - lon1

    a = sin(difLat/2)**2 + (cos(lat1) * cos(lat2) * sin(difLon/2)**2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = 6371 * c

    return distance

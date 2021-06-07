"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

connectionsFile = 'connections.csv'
countriesFile = 'countries.csv'
LpFile = 'landing_points.csv'
InitialPoint = None


def printMenu():
    print("Bienvenido")
    print("1- Inicializar catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Identificar clusteres de comunicacion")
    print("4- Identificar puntos de conexion criticos en la red")
    print("5- Identificar ruta de menor distancia")
    print("6- Identificar Infraestructura critica de la red")
    print("7- Analisis de fallas")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        catalog = controller.init()
        print('Se inicializo el catalogo\n')

    elif int(inputs[0]) == 2:
        print("\nCargando información de los archivos ....")
        controller.loadConnections(catalog, connectionsFile)
        r2 = controller.loadCountries(catalog, countriesFile)
        r1 = controller.loadLp(catalog, LpFile)
        print("Se cargo la informacion del catalogo\n")
        numVert = controller.totalVertex(catalog)
        numArcos = controller.totalConnections(catalog)
        numCountries = controller.totalCountries(catalog)
        primer_lp = r1[1]
        ultimo_pais = r2[1]

        print('Total de landing points: ' + str(numVert))
        print('Total de conexiones: ' + str(numArcos))
        print('Total de Paises: ' + str(numCountries))
        print('Informacion del primer landing point cargado: ' + 'Identificador: ' + primer_lp['landing_point_id'] + ', Nombre: ' + primer_lp['name'] +
              ', Latitud: ' + primer_lp['latitude'] + ', Longitud: ' + primer_lp['longitude'])
        print('Informacion del ultimo pais cargado: ' + ' Poblacion: ' + ultimo_pais['Population'] + 
              ', Usuarios de internet: ' + ultimo_pais['Internet users'])

    elif int(inputs[0]) == 3:
        lp1 = input('Ingrese el landing point de inicio: ')
        lp2 = input('Ingrese el landing point final: ')
        r = controller.getClusters(catalog, lp1, lp2)
        print('El numero de clusteres es: ' + str(r[0]))
        print('¿Los landing points ingresados estan fuertemente conectados?: ' + str(r[1]))
    else:
        sys.exit(0)
sys.exit(0)

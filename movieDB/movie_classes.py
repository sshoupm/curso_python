'''Clases para manejar la base de datos de películas'''
import csv
import os
import hashlib
from datetime import datetime

class Actor:
    '''Clase para manejar la información de un actor'''
    def __init__(self, id_estrella, nombre, fecha_nacimiento, ciudad_nacimiento, url_imagen, username):
        self.id_estrella            = id_estrella
        self.nombre                 = nombre
        self.fecha_nacimiento       = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        self.ciudad_nacimiento      = ciudad_nacimiento
        self.url_imagen             = url_imagen
        self.username               = username

    def to_dict(self):
        '''Devuelve un diccionario con los datos del actor'''
        return {'id_estrella':self.id_estrella, 
                'nombre':self.nombre, 
                'fecha_nacimiento': self.fecha_nacimiento.strftime('%Y-%m-%d'),
                'ciudad_nacimiento':self.ciudad_nacimiento, 
                'url_imagen':self.url_imagen, 
                'username':self.username
                }
    
class Pelicula:
    '''Clase para manejar la información de una película'''
    def __init__(self, id_pelicula, titulo_pelicula, fecha_lanzamiento, url_poster):
        '''Inicializa la clase con los datos de la película'''
        self.id_pelicula            = id_pelicula
        self.titulo_pelicula        = titulo_pelicula
        self.fecha_lanzamiento      = datetime.strptime(fecha_lanzamiento, '%Y-%m-%d').date()
        self.url_poster             = url_poster
    def to_dict(self):
        '''Devuelve un diccionario con los datos de la película'''
        return {'id_pelicula':self.id_pelicula, 
                'titulo_pelicula':self.titulo_pelicula, 
                'fecha_lanzamiento':self.fecha_lanzamiento.strftime('%Y-%m-%d'),
                'url_poster':self.url_poster
                }
    
class Relaciones:
    '''Clase para manejar las relaciones entre actores y películas'''
    def __init__(self, id_relacion, id_pelicula, id_estrella):
        '''Inicializa la clase con los datos de la relación'''
        self.id_relacion            = id_relacion
        self.id_pelicula            = id_pelicula
        self.id_estrella            = id_estrella
    def to_dict(self):
        '''Devuelve un diccionario con los datos de la relación'''
        return {'id_relacion':self.id_relacion, 
                'id_pelicula':self.id_pelicula, 
                'id_estrella':self.id_estrella
                }

class User:
    '''Clase para manejar la información de un usuario'''
    def __init__(self, username, nombre_completo, email, password):
        '''Inicializa la clase con los datos del usuario'''
        self.username               = username
        self.nombre_completo        = nombre_completo
        self.email                  = email
        self.password               = password
    def to_dict(self):
        '''Devuelve un diccionario con los datos del usuario'''
        return {'username':self.username, 
                'nombre_completo':self.nombre_completo, 
                'email':self.email,
                'password':self.password,
                }
    def hash_string(self, string):
        '''Devuelve el hash de un string'''
        return hashlib.sha256(string.encode()).hexdigest()

class SistemaCine:
    '''Clase para manejar la información de un sistema de cine'''
    def __init__(self):
        '''Inicializa la clase con los datos del sistema'''
        self.actores = {}
        self.peliculas = {}
        self.relaciones = {}
        self.usuarios = {}
    def cargar_csv(self, archivo, clase):
        '''Carga los datos de un archivo CSV en la base de datos'''
        with open(archivo, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if clase == Actor:
                    actor = Actor(**row)
                    self.actores[actor.id_estrella] = actor
                elif clase == Pelicula:
                    pelicula = Pelicula(**row)
                    self.peliculas[pelicula.id_pelicula] = pelicula
                elif clase == Relaciones:
                    relaciones = Relaciones(**row)
                    self.relaciones[relaciones.id_relacion] = relaciones
                elif clase == User:
                    user = User(**row) 
                    self.usuarios[user.username] = user

if __name__ == "__main__":
    #archivo='datos/actores.csv'
    archivo_actores="datos/movies_db - actores.csv"
    archivo_peliculas="datos/movies_db - peliculas.csv"
    archivo_relaciones="datos/movies_db - relacion.csv"
    archivo_usuarios="datos/movies_db - users.csv"
    sistema = SistemaCine()
    sistema.cargar_csv(archivo_actores, Actor)
    sistema.cargar_csv(archivo_peliculas, Pelicula)
    sistema.cargar_csv(archivo_relaciones, Relaciones)
    sistema.cargar_csv(archivo_usuarios, User)
    actores=sistema.actores
    for id_estrella, actor in actores.items():
        print(f"{id_estrella}: {actor.nombre:35s} - {actor.fecha_nacimiento}")
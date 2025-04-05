'''Programa principal de MovieDB'''
from flask import Flask, flash, request, session, url_for, render_template, redirect
import os
import random
import movie_classes as mc

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para la sesión
sistema = mc.SistemaCine()
archivo_actores = "datos/movies_db - actores.csv"
archivo_peliculas = "datos/movies_db - peliculas.csv"
archivo_relacion = "datos/movies_db - relacion.csv"
archivo_users = "datos/movies_db - users_hashed.csv"
sistema.cargar_csv(archivo_actores, mc.Actor)
sistema.cargar_csv(archivo_peliculas, mc.Pelicula)
sistema.cargar_csv(archivo_relacion, mc.Relacion)
sistema.cargar_csv(archivo_users, mc.Users)

@app.route('/')
def index():
    '''Pagina principal de la palicación'''
    return render_template('index.html')

@app.route('/actores')
def actores():
    '''Muestra la lista de actores'''
    actores = sistema.actores.values()
    return render_template('actores.html', actores=actores)

'''
@app.route('/actor/<int:id_actor>')
def actor(id_actor):
    'Muestra la información de un actor'
    actor = sistema.actores.get(id_actor)
    peliculas= sistema.obtener_peliculas_y_personajes_por_actor(id_actor)
    if not actor:
        return "Actor no encontrado", 404
    return render_template('actor.html', actor=actor, peliculas=peliculas)
'''
@app.route('/actor/<int:id_actor>')
def actor(id_actor):
    '''Muestra la información de un actor'''
    actor = sistema.actores[id_actor]
    personajes = sistema.obtener_personajes_por_estrella(id_actor)
    return render_template('actor.html', actor=actor, lista_peliculas=personajes)	

@app.route('/peliculas')
def peliculas():
    '''Muestra la lista de peliculas'''
    peliculas = sistema.peliculas.values()
    return render_template('peliculas.html', peliculas=peliculas)

'''
@app.route('/pelicula/<int:id_pelicula>')
def pelicula(id_pelicula):
    'Muestra la información de una película'
    pelicula = sistema.peliculas.get(id_pelicula)
    actores = sistema.obtener_actores_y_personajes_por_pelicula(id_pelicula)
    if not pelicula:
        return "Película no encontrada", 404
    return render_template('pelicula.html', pelicula=pelicula, actores=actores)'
'''
@app.route('/pelicula/<int:id_pelicula>')
def pelicula(id_pelicula):
    '''Muestra la información de una película'''
    pelicula = sistema.peliculas[id_pelicula]
    actores = sistema.obtener_personajes_por_pelicula(id_pelicula)
    return render_template('pelicula.html', pelicula=pelicula, lista_actores=actores)

@app.route('/agregar_peliculas', methods=['GET', 'POST'])
def agregar_pelicula():
    if sistema.usuario_actual is None:
        flash('Debes iniciar sesión para agregar películas', 'warning')
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('agregar_pelicula.html')
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        fecha_lanzamiento = request.form.get('fecha_lanzamiento')
        url_poster = request.form.get('url_poster')
        sistema.agregar_pelicula(titulo,fecha_lanzamiento,url_poster)
        sistema.guardar_csv(archivo_peliculas,sistema.peliculas)
        return redirect(url_for('peliculas'))
    
@app.route('/agregar_actores', methods=['GET', 'POST'])
def agregar_actor():
    if sistema.usuario_actual is None:
        flash('Debes iniciar sesión para agregar actores', 'warning')
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('agregar_actor.html')
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        ciudad_nacimiento = request.form.get('ciudad_nacimiento')
        url_imagen = request.form.get('url_imagen')
        sistema.agregar_actor(nombre,fecha_nacimiento,ciudad_nacimiento,url_imagen)
        sistema.guardar_csv(archivo_actores,sistema.actores)
        return redirect(url_for('actores'))
    
@app.route('/agregar_relacion', methods=['GET', 'POST'])
def agregar_relacion():
    '''Agrega una relaciión entre un actor y una película'''
    if sistema.usuario_actual is None:
        flash('Debes iniciar sesión para agregar relaciones', 'warning')
        return redirect(url_for('login'))
    if request.method=='GET':
        actores_list=[]
        for actor in sistema.actores.values():
            actores_list.append({
                'id_estrella': actor.id_estrella,
                'nombre': actor.nombre
            })
            sorted_actores = sorted(actores_list, key=lambda x: x['nombre'])
        peliculas_list=[]
        for pelicula in sistema.peliculas.values():
            peliculas_list.append({
                'id_pelicula': pelicula.id_pelicula,
                'titulo': pelicula.titulo_pelicula
            })
            sorted_peliculas = sorted(peliculas_list, key=lambda x: x['titulo'])
        return render_template('agregar_relacion.html', actores=sorted_actores, peliculas=sorted_peliculas)
    if request.method == 'POST':
        id_actor= int(request.form['actorSelect'])
        id_pelicula = int(request.form['movieSelect'])
        personaje = request.form['character']
        sistema.agregar_relacion(id_pelicula, id_actor, personaje)
        sistema.guardar_csv(archivo_relacion,sistema.relacion)
        flash('Relación agregada correctamente', 'success')
        return redirect(url_for('actor', id_actor=id_actor))

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Muestra el formulario de login'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        exito = sistema.login(username, password)
        if exito:
            session['logged_in'] = True
            session['username'] = sistema.usuario_actual.nombre_completo
            return redirect(url_for('index'))
        else:
            error = "Usuario o contraseña incorrectos"
            return render_template('login.html')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from app.models.track import Track
from app.models.genre import Genre
from app.database import init_app, init_db

d = os.path.dirname(__file__)
os.chdir(d)

# Configuración inicial
app = Flask(__name__)
CORS(app)
init_app(app)

# Ruta para inicializar la base de datos
@app.route('/init-db')
def init_db_route():
    init_db()
    return "Base de datos inicializada correctamente."

# Ruta principal
@app.route('/')
def principal():
    return "¡Hola! Esta es la API para gestionar pistas musicales y géneros."

### Gestión de Pistas Musicales ###

# Crear una pista
@app.route('/tracks', methods=['POST'])
def create_track():
    data = request.json
    nuevo_track = Track(
        title=data['title'], 
        artist=data['artist'], 
        album=data.get('album', ''), 
        release_year=data.get('release_year', 2024), 
        cover_url=data.get('cover_url', ''), 
        preview_url=data.get('preview_url', '')
    )
    nuevo_track.save()

    # Asociar los géneros a la pista en la tabla tracks_genres
    genres = data.get('genres', [])  # Lista de IDs de géneros que pertenecen a la pista
    for genre_id in genres:
        nuevo_track.add_genre(genre_id)
    return jsonify({'message': 'Pista creada correctamente'}), 201

# Obtener todas las pistas
@app.route('/tracks', methods=['GET'])
def get_all_tracks():
    tracks = Track.get_all()
    return jsonify([track.serialize() for track in tracks])

# Obtener una pista por su ID
@app.route('/tracks/<int:id_track>', methods=['GET'])
def get_by_id_track(id_track):
    track = Track.get_by_id(id_track)
    if track:
        return jsonify(track.serialize())
    else:
        return jsonify({'message': 'Pista no encontrada'}), 404

# Eliminar una pista por su ID
@app.route('/tracks/<int:id_track>', methods=['DELETE'])
def delete_track(id_track):
    track = Track.get_by_id(id_track)
    if not track:
        return jsonify({'message': 'Pista no encontrada'}), 404
    track.delete()
    return jsonify({'message': 'La pista fue eliminada correctamente'})

# Actualizar una pista por su ID
@app.route('/tracks/<int:id_track>', methods=['PUT'])
def update_track(id_track):
    track = Track.get_by_id(id_track)
    if not track:
        return jsonify({'message': 'Pista no encontrada'}), 404
    data = request.json
    track.title = data.get('title', track.title)
    track.artist = data.get('artist', track.artist)
    track.album = data.get('album', track.album)
    track.release_year = data.get('release_year', track.release_year)
    track.cover_url = data.get('cover_url', track.cover_url)
    track.preview_url = data.get('preview_url', track.preview_url)
    track.save()
    return jsonify({'message': 'Pista actualizada correctamente'})

### Gestión de Géneros ###

# Crear un género
@app.route('/genres', methods=['POST'])
def create_genre():
    data = request.json
    nuevo_genre = Genre(name=data['name'])
    nuevo_genre.save()
    return jsonify({'message': 'Género creado correctamente'}), 201

# Obtener todos los géneros
@app.route('/genres', methods=['GET'])
def get_all_genres():
    genres = Genre.get_all()
    return jsonify([genre.serialize() for genre in genres])

# Obtener un género por su ID
@app.route('/genres/<int:id_genre>', methods=['GET'])
def get_by_id_genre(id_genre):
    genre = Genre.get_by_id(id_genre)
    if genre:
        return jsonify(genre.serialize())
    else:
        return jsonify({'message': 'Género no encontrado'}), 404

# Eliminar un género por su ID
@app.route('/genres/<int:id_genre>', methods=['DELETE'])
def delete_genre(id_genre):
    genre = Genre.get_by_id(id_genre)
    if not genre:
        return jsonify({'message': 'Género no encontrado'}), 404
    genre.delete()
    return jsonify({'message': 'El género fue eliminado correctamente'})

# Actualizar un género por su ID
@app.route('/genres/<int:id_genre>', methods=['PUT'])
def update_genre(id_genre):
    genre = Genre.get_by_id(id_genre)
    if not genre:
        return jsonify({'message': 'Género no encontrado'}), 404
    data = request.json
    genre.name = data.get('name', genre.name)
    genre.save()
    return jsonify({'message': 'Género actualizado correctamente'})

# Ejecutar la aplicación si este archivo es el punto de entrada principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import os 
# pip install mysql-connector-python
import mysql.connector  # Importa el conector MySQL para conectar con la base de datos
from flask import g  # Importa g de Flask para almacenar datos durante la petición
# pip install python-dotenv
from dotenv import load_dotenv  

d = os.path.dirname(__file__)
os.chdir(d)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos usando variables de entorno
# DATABASE_CONFIG = {
#     'user': os.getenv('DB_USERNAME'),  
#     'password': os.getenv('DB_PASSWORD'),  
#     'host': os.getenv('DB_HOST'),  
#     'database': os.getenv('DB_NAME'),  
#     'port': os.getenv('DB_PORT', 3306)  # Puerto del servidor de la base de datos, por defecto es 3306 si no se especifica
# }

DATABASE_CONFIG = {
    'user':"sql5717608",  
    'password': "4mx2jA9Ds2",  
    'host': "sql5.freemysqlhosting.net",  
    'database': "sql5717608",  
    'port': 3306  # Puerto del servidor de la base de datos, por defecto es 3306 si no se especifica
}


# Función para obtener la conexión de la base de datos
def get_db():
    # Si no hay una conexión a la base de datos en g, la creamos
    # g, que es un objeto de Flask que se usa para almacenar datos durante la vida útil de una solicitud.
    if 'db' not in g:
        print("···· Abriendo conexion a DB ····",DATABASE_CONFIG['database']," ---- ",DATABASE_CONFIG['user'])
        g.db = mysql.connector.connect(**DATABASE_CONFIG)
    # Retorna la conexión a la base de datos
    return g.db

# Función para cerrar la conexión a la base de datos
def close_db(e=None):
    # Intenta obtener la conexión de la base de datos desde g
    db = g.pop('db', None)
    # Si hay una conexión, la cerramos
    if db is not None:
        print("···· Cerrando conexion a DB ····")
        db.close()
# Función para inicializar la base de datos
def init_db():
    db = get_db()
    cursor = db.cursor()

    # Crear tablas si no existen con todas las claves e índices incluidos
    sql_commands = [
    """CREATE TABLE IF NOT EXISTS `tracks` (
        `id_track` INT NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(100) NOT NULL,
        `artist` VARCHAR(100) NOT NULL,
        `album` VARCHAR(100),
        `release_year` INT DEFAULT 2024,
        `cover_url` VARCHAR(200),
        `preview_url` VARCHAR(200),
         PRIMARY KEY (`id_track`)
    );""",
    
    """CREATE TABLE IF NOT EXISTS `genres` (
        `id_genre` INT NOT NULL AUTO_INCREMENT,
        `name` VARCHAR(45) NOT NULL,
         PRIMARY KEY (`id_genre`),
         UNIQUE KEY `name_UNIQUE` (`name`)
    );""",
    
    """CREATE TABLE IF NOT EXISTS `tracks_genres` (
        `id_track_genre` INT NOT NULL AUTO_INCREMENT,
        `id_track` INT DEFAULT NULL,
        `id_genre` INT DEFAULT NULL,
        PRIMARY KEY (`id_track_genre`),
        KEY `FK1_track_idx` (`id_track`),
        KEY `FK2_genre_idx` (`id_genre`),
        CONSTRAINT `FK1_track` FOREIGN KEY (`id_track`) REFERENCES `tracks` (`id_track`) ON DELETE CASCADE,
        CONSTRAINT `FK2_genre` FOREIGN KEY (`id_genre`) REFERENCES `genres` (`id_genre`) ON DELETE CASCADE
    );"""
    
   
]

    for command in sql_commands:
        cursor.execute(command)

    db.commit()

    # Inserciones de géneros si no existen
    cursor.execute("""
        INSERT INTO genres (name) VALUES
         ('Pop'), ('Rock'), ('Jazz'), ('Hip-Hop'), ('Clásica'),
         ('Reggae'), ('Blues'), ('Metal'), ('Country'), ('Electrónica')
        ON DUPLICATE KEY UPDATE name=name;
    """),
    
    #"""INSERT INTO tracks (title, artist, album, release_year, cover_url, preview_url) VALUES
    #   ('Song 1', 'Artist 1', 'Album 1', 2024, 'cover1.jpg', 'preview1.mp3'),
    #   ('Song 2', 'Artist 2', 'Album 2', 2023, 'cover2.jpg', 'preview2.mp3');
    #"""
    
    db.commit()
    cursor.close()

# Función para inicializar la aplicación con el cierre automático de la conexión a la base de datos
def init_app(app):
    # Registrar la función close_db para que se llame automáticamente
    # cuando el contexto de la aplicación se destruye
    app.teardown_appcontext(close_db)

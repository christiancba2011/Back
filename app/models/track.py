from app.database import get_db

class Track:
    def __init__(self, id_track=None, title=None, artist=None, album=None, release_year=None, cover_url=None, preview_url=None, genres=[]):
        self.id_track = id_track
        self.title = title
        self.artist = artist
        self.album = album
        self.release_year = release_year
        self.cover_url = cover_url
        self.preview_url = preview_url
        self.genres = genres

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_track:
            cursor.execute("""
                UPDATE tracks SET title = %s, artist = %s, album = %s, release_year = %s, cover_url = %s, preview_url = %s
                WHERE id_track = %s
            """, (self.title, self.artist, self.album, self.release_year, self.cover_url, self.preview_url, self.id_track))
        else:
            cursor.execute("""
                INSERT INTO tracks (title, artist, album, release_year, cover_url, preview_url) VALUES (%s, %s, %s, %s, %s, %s)
            """, (self.title, self.artist, self.album, self.release_year, self.cover_url, self.preview_url))
            self.id_track = cursor.lastrowid
        db.commit()

        # Actualizar relación tracks_genres
        cursor.execute("DELETE FROM tracks_genres WHERE id_track = %s", (self.id_track,))
        for genre_id in self.genres:
            cursor.execute("INSERT INTO tracks_genres (id_track, id_genre) VALUES (%s, %s)", (self.id_track, genre_id))
        db.commit()

        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_track, title, artist, album, release_year, cover_url, preview_url FROM tracks")
        rows = cursor.fetchall()

        tracks = []
        for row in rows:
            track = Track(id_track=row[0], title=row[1], artist=row[2], album=row[3], release_year=row[4], cover_url=row[5], preview_url=row[6])
            track.genres = Track.get_genres_of_track(track.id_track)
            tracks.append(track)

        cursor.close()
        return tracks

    @staticmethod
    def get_by_id(id_track):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_track, title, artist, album, release_year, cover_url, preview_url FROM tracks WHERE id_track = %s", (id_track,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            track = Track(id_track=row[0], title=row[1], artist=row[2], album=row[3], release_year=row[4], cover_url=row[5], preview_url=row[6])
            track.genres = Track.get_genres_of_track(id_track)
            return track
        else:
            return None

    @staticmethod
    def get_genres_of_track(id_track):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT g.id_genre, g.name
            FROM tracks_genres tg
            JOIN genres g ON tg.id_genre = g.id_genre
            WHERE tg.id_track = %s
        """, (id_track,))
        genres = cursor.fetchall()
        cursor.close()
        return genres

    def add_genre(self, id_genre):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO tracks_genres (id_track, id_genre) VALUES (%s, %s)", (self.id_track, id_genre))
        db.commit()
        cursor.close()

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM tracks WHERE id_track = %s", (self.id_track,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'id_track': self.id_track,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'release_year': self.release_year,
            'cover_url': self.cover_url,
            'preview_url': self.preview_url,
            'genres': [{'id_genre': genre[0], 'name': genre[1]} for genre in self.genres]
        }

    def __str__(self):
        return f"TRACK: {self.id_track} - {self.title} by {self.artist}"

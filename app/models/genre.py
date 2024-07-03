from app.database import get_db

class Genre:
    def __init__(self, id_genre=None, name=None):
        self.id_genre = id_genre
        self.name = name

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_genre:
            cursor.execute("UPDATE genres SET name = %s WHERE id_genre = %s", (self.name, self.id_genre))
        else:
            cursor.execute("INSERT INTO genres (name) VALUES (%s)", (self.name,))
            self.id_genre = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_genre, name FROM genres")
        rows = cursor.fetchall()
        genres = [Genre(id_genre=row[0], name=row[1]) for row in rows]
        cursor.close()
        return genres

    @staticmethod
    def get_by_id(id_genre):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_genre, name FROM genres WHERE id_genre = %s", (id_genre,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Genre(id_genre=row[0], name=row[1])
        else:
            return None

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM genres WHERE id_genre = %s", (self.id_genre,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'id_genre': self.id_genre,
            'name': self.name
        }

    def __str__(self):
        return f"GENRE: {self.id_genre} - {self.name}"

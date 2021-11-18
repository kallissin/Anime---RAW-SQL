from psycopg2 import sql
from app.models import close_and_commit, conn_cur
from app.models.exceptions import TypeKeyError


class Anime:
    def __init__(self, fields):
        if (type(fields) is dict):
            for key, value in fields.items():
                setattr(self, key, value)
        elif (type(fields) is tuple):
            self.id, self.anime, self.released_date, self.seasons = fields


    @staticmethod
    def create_table():
        conn, cur = conn_cur()

        query = """
            CREATE TABLE IF NOT EXISTS animes(
                id BIGSERIAL PRIMARY KEY,
                anime VARCHAR(100) NOT NULL UNIQUE,    
                released_date DATE NOT NULL,
                seasons INTEGER NOT NULL        
            );
        """
        
        cur.execute(query)

        close_and_commit(conn, cur)


    @staticmethod
    def get_all():
        conn, cur = conn_cur()

        query = sql.SQL("""
            SELECT * FROM {table}
        """).format(table=sql.Identifier('animes'))

        cur.execute(query)

        list_animes = cur.fetchall()

        close_and_commit(conn, cur)

        return [Anime(anime).__dict__ for anime in list_animes]

    def create_anime(self):
        conn, cur = conn_cur()

        column = [sql.Identifier(key) for key in self.__dict__.keys()]
        values = [sql.Literal(value) for value in self.__dict__.values()]

        query = sql.SQL("""
            INSERT INTO animes
                ({column})
            VALUES
                ({values})
            RETURNING *
        """).format(column=sql.SQL(',').join(column), values=sql.SQL(',').join(values))

        cur.execute(query)

        insert_anime = cur.fetchone()

        close_and_commit(conn, cur)

        return Anime(insert_anime).__dict__

    @staticmethod
    def get_by_id(anime_id):
        conn, cur = conn_cur()

        query = sql.SQL("""
            SELECT * 
            FROM animes
            WHERE id = {anime_id}
        """).format(anime_id=sql.Literal(anime_id))

        cur.execute(query)

        get_anime = cur.fetchone()

        close_and_commit(conn, cur)

        return Anime(get_anime).__dict__


    @staticmethod
    def validate_key(data):
        type_key = ['anime', 'released_date', 'seasons']
        print(data)
        for key in data.keys():
            if key not in type_key:
                raise TypeKeyError(data.keys())
    

    @staticmethod
    def format_key_anime(data):
        data['anime'] = data['anime'].title()
        return data
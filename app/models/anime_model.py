from app.models import close_and_commit, conn_cur


class Anime:
    def __init__(self, anime: str, released_date: str, seasons: int):
        self.anime = anime
        self.released_date = released_date
        self.seasons = seasons

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

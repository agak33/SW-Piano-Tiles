import sqlite3


class Database(object):
    def __init__(self):
        self.connection = sqlite3.connect('database/base.db')
        self.cursor     = self.connection.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ranking(
                gameName varchar2 NOT NULL,
                name varchar2,
                points number NOT NULL
                )
        ''')

    def saveGame(self, gameName: str, name: str, points: int) -> None:
        self.connection.execute('''
            INSERT INTO ranking(gameName, name, points) 
            VALUES(?, ?, ?)
        ''', (gameName, name, points))
        self.connection.commit()

    def getRanking(self):
        self.cursor.execute('''
            SELECT * FROM ranking
            ORDER BY points DESC
        ''')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

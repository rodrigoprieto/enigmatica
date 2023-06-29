import sqlite3
from sqlite3 import Error

class UserDatabase:
    def __init__(self, db_file):

        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            self.conn.row_factory = sqlite3.Row
        except Error as e:
            print(e)

        if self.conn:
            self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, language_code TEXT)
        ''')

    def insert_user(self, user):
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO users VALUES(?,?,?,?)
        ''', (user.id,
              user.username,
              user.first_name,
              user.language_code,
              ))
        self.conn.commit()

    def get_user(self, id):
        c = self.conn.cursor()
        c.execute('SELECT * FROM users WHERE id=?', (id,))
        return c.fetchone()

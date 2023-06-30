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
            self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, language_code TEXT)
        ''')
        c.execute('''
                    CREATE TABLE IF NOT EXISTS users_enigmas
                    (user_id INTEGER, enigma_id INTEGER, PRIMARY KEY (user_id, enigma_id))
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


    def save_solved_enigma(self, user_id, enigma_id):
        c = self.conn.cursor()
        c.execute('INSERT OR IGNORE INTO users_enigmas (user_id, enigma_id) VALUES (?,?)',
                  (user_id, enigma_id))
        self.conn.commit()


    def get_enigmas_solved_by_user(self, id):
        c = self.conn.cursor()
        c.execute('SELECT enigma_id FROM users_enigmas WHERE user_id=?', (id,))
        enigmas_ids = c.fetchall()
        enigma_list = []
        for enigma_id in enigmas_ids:
            enigma_list.append(enigma_id[0]) # Get the id
        return enigma_list


    def reset_enigmas_by_user(self, id):
        c = self.conn.cursor()
        c.execute('DELETE FROM users_enigmas WHERE user_id=?', (id,))
        self.conn.commit()

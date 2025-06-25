import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("Users.db")
        self.cursor = self.conn.cursor()
        self.create_table("users", "username", "password")

    def create_table(self, table_name, column1, column2):
        try:
            self.cursor.execute(f'''CREATE TABLE {table_name}(id INTEGER PRIMARY KEY AUTOINCREMENT , {column1} TEXT, {column2} TEXT)''')
        except: pass

    def add(self, username, password, column1="username", column2="password", table="users"):
        self.cursor.execute(f"INSERT INTO {table}({column1}, {column2}) VALUES (?, ?)", (username, password))
        self.conn.commit()

    def check_username(self, username, table="users"):
        self.cursor.execute(f"SELECT username FROM {table} WHERE username=?", (username,))
        result = self.cursor.fetchone()
        return result

    def check_password(self, username, password):
        self.cursor.execute(f"SELECT password FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        if result and password == result[0]:
            return True
        else:
            return False

    def get_content(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        result = self.cursor.fetchall()
        return result

    def get_id(self, username):
        self.cursor.execute(f"SELECT id FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        return result

    def update(self, table, user, text):
        self.cursor.execute(f"""UPDATE {table} SET conversation = conversation || ? WHERE username = ?""", (text, user))
        self.conn.commit()

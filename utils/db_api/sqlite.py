import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id int NOT NULL,
            fullname VARCHAR(2555),
            phone VARCHAR(25),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def add_user(self, id, fullname, phone):

        sql = """
        INSERT INTO Users(id, fullname, phone) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, fullname, phone), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, id):
        sql = f"SELECT * FROM Users WHERE id='{id}'"
        return self.execute(sql, fetchone=True)

    def update_user_ism(self, fullname, id):
        sql = f"""UPDATE Users SET fullname='{fullname}' WHERE id='{id}'"""
        self.execute(sql, commit=True)

    def update_user_phone(self, phone, id):
        sql = f"""UPDATE Users SET phone='{phone}' WHERE id='{id}'"""
        self.execute(sql, commit=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def create_table_keyboard(self):
        sql = """
        CREATE TABLE IF NOT EXISTS keyboard (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        types VARCHAR(255),
        text VARCHAR(255)
        );
    """
        self.execute(sql, commit=True)

    def add_keyboard(self, types, text):
        sql = """
           INSERT INTO keyboard(types, text) VALUES(?, ?)
           """
        self.execute(sql,parameters=(types, text), commit=True)

    def select_all_keyboard(self, types):
        sql = f"""
           SELECT * FROM keyboard WHERE types='{types}'
           """
        return self.execute(sql, fetchall=True)

    def delete_keayboards(self):
        self.execute("DELETE FROM keyboard WHERE TRUE", commit=True)

    def create_table_mashq(self):
        sql = """
        CREATE TABLE IF NOT EXISTS mashq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        daraja VARCHAR(255) NOT NULL,
        mashq VARCHAR(255) NOT NULL,
        savol VARCHAR(2555),
        javob VARCHAR(2555),
        izoh VARCHAR(255)
        );
    """
        self.execute(sql, commit=True)

    def add_mashq(self, daraja, mashq, savol, javob, izoh:None):
        sql = """
           INSERT INTO mashq( daraja, mashq, savol, javob, izoh) VALUES(?, ?, ?, ?, ?)
           """
        self.execute(sql,parameters=( daraja, mashq, savol, javob, izoh), commit=True)

    def select_all_mashq(self, daraja, mashq):
        sql = f"""
           SELECT * FROM mashq WHERE daraja='{daraja}' AND mashq='{mashq}'
           """
        return self.execute(sql, fetchall=True)

    def select_mashq(self, id):
        sql = f"""
           SELECT * FROM mashq WHERE id='{id}'
           """
        return self.execute(sql, fetchone=True)

    def update_mashq_savol(self, savol, id):
        sql = f"""UPDATE mashq SET savol='{savol}' WHERE id='{id}'"""
        self.execute(sql, commit=True)

    def update_mashq_javob(self, javob, id):
        sql = f"""UPDATE mashq SET javob='{javob}' WHERE id='{id}'"""
        self.execute(sql, commit=True)


    def update_mashq_izoh(self, izoh, id):
        sql = f"""UPDATE mashq SET izoh='{izoh}' WHERE id='{id}'"""
        self.execute(sql, commit=True)

    def delete_mashq(self):
        self.execute("DELETE FROM mashq WHERE TRUE", commit=True)

    def create_table_admin(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY
        );
    """
        self.execute(sql, commit=True)

    def add_admin(self, id):
        sql = f"""
           INSERT INTO admins (id) VALUES('{id}')
           """
        self.execute(sql, commit=True)

    def select_admin(self, id):
        sql = f"""
           SELECT * FROM admins WHERE id='{id}'
           """
        return self.execute(sql, fetchone=True)

    def select_all_admin(self):
        sql = f"""
           SELECT * FROM admins
           """
        return self.execute(sql, fetchall=True)

    def delete_admin(self, id):
        self.execute(f"DELETE FROM admins WHERE id='{id}'", commit=True)

def logger(statement):
    pass

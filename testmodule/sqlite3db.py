import sqlite3
import traceback
import sys


class FPAttendanceSystemDB:

    def __init__(self) -> None:
        super().__init__()
        self.sqliteConnection = sqlite3.connect('SQLite_Python.db')

    def create_db(self):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS register_fp (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        joining_date datetime,
                                        image_id TEXT);'''

            cursor = self.sqliteConnection.cursor()

            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            self.sqliteConnection.commit()
            print("SQLite table created")

            cursor.close()
            self.sqliteConnection.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)

    def insert_data(self, name, joining_date, image_id):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_insert_query = """INSERT INTO register_fp
                              (name, joining_date, image_id) 
                              VALUES (?, ?, ?);"""
            cursor.execute(sqlite_insert_query, (name, joining_date, image_id))

            # sql_update_query = """Update SqliteDb_developers set salary = 10000 where id = 4"""
            # cursor.execute(sql_update_query)
            #
            # sql_delete_query = """DELETE from SqliteDb_developers where id = 4"""
            # cursor.execute(sql_delete_query)

            self.sqliteConnection.commit()
            cursor.close()

            print("Total Rows affected since the database connection was opened: ", self.sqliteConnection.total_changes)
            self.sqliteConnection.close()
            print("sqlite connection is closed")

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def select_registered_fp(self, fp_id):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            rows = cursor.execute("""SELECT name, fp_id FROM register_fp WHERE fp_id in (values(?))""", fp_id)

            for row in rows:
                print(row)

            self.sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def attendance_table(self):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS fp_att (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        status TEXT,
                                        checkin_time datetime,
                                        exit_status TEXT,
                                        checkout_time datetime,
                                        fp_id TEXT);'''

            cursor = self.sqliteConnection.cursor()

            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            self.sqliteConnection.commit()
            print("SQLite table created")

            cursor.close()
            self.sqliteConnection.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)

    def insert_attendance(self, name, status, checkin_time, exit_status, checkout_time, fp_id):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_insert_query = """INSERT INTO fp_att
                              (name, status, checkin_time, exit_status, checkout_time, fp_id) 
                              VALUES (?, ?, ?);"""
            cursor.execute(sqlite_insert_query, (name, status, checkin_time, exit_status, checkout_time, fp_id))

            # sql_update_query = """Update SqliteDb_developers set salary = 10000 where id = 4"""
            # cursor.execute(sql_update_query)
            #
            # sql_delete_query = """DELETE from SqliteDb_developers where id = 4"""
            # cursor.execute(sql_delete_query)

            self.sqliteConnection.commit()
            cursor.close()

            print("Total Rows affected since the database connection was opened: ", self.sqliteConnection.total_changes)
            self.sqliteConnection.close()
            print("sqlite connection is closed")

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def select_fp_attendance_record(self, fp_id):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            rows = cursor.execute("""SELECT name, fp_id FROM fp_att WHERE fp_id in (values(?))""", fp_id)

            for row in rows:
                print(row)

            self.sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)


att = FPAttendanceSystemDB()
att.insert_data('Jonson', "2022-11-10", '21')

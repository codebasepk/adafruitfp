import datetime
import sqlite3
import traceback
import sys


class FPAttendanceSystemDB:

    def __init__(self) -> None:
        super().__init__()
        self.sqliteConnection = sqlite3.connect('fp_attendance_db.db')
        self.create_db_table()
        self.attendance_table()

    def create_db_table(self):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS register_fp (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        joining_date timestamp,
                                        image_id INTEGER UNIQUE);'''

            cursor = self.sqliteConnection.cursor()

            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            self.sqliteConnection.commit()
            print("SQLite table created")

            # cursor.close()
            # self.sqliteConnection.close()

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
            # cursor.close()

            print("Total Rows affected since the database connection was opened: ", self.sqliteConnection.total_changes)
            # self.sqliteConnection.close()
            print("sqlite connection is closed")

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def select_registered_fp(self, fp_id):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            rows = cursor.execute("""SELECT name, image_id, joining_date FROM register_fp 
            WHERE image_id in (values(?))""", [fp_id])
            row = cursor.fetchone()
            # print("row", row)
            # for row in rows:
            #     # ext_id = row[0]
            #     print(row)

            # self.sqliteConnection.commit()
            cursor.close()
            return row

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def attendance_table(self):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS fp_att (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        status TEXT,
                                        cur_date DATE,
                                        checkin_time TEXT,
                                        exit_status TEXT,
                                        checkout_time TEXT,
                                        fp_id INTEGER);'''

            cursor = self.sqliteConnection.cursor()

            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            self.sqliteConnection.commit()
            print("SQLite table created")

            # cursor.close()
            # self.sqliteConnection.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)

    def insert_attendance(self, name, cur_date, checkin_time, fp_id):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_insert_query = """INSERT INTO fp_att
                              (name, status, cur_date, checkin_time, exit_status, checkout_time, fp_id) 
                              VALUES (?, 'Not Marked', ?, ?, 'Not Marked', '', ?);"""
            cursor.execute(sqlite_insert_query, (name, cur_date, checkin_time, fp_id))

            # sql_update_query = """Update SqliteDb_developers set salary = 10000 where id = 4"""
            # cursor.execute(sql_update_query)
            #
            # sql_delete_query = """DELETE from SqliteDb_developers where id = 4"""
            # cursor.execute(sql_delete_query)

            self.sqliteConnection.commit()
            # cursor.close()

            print("Total Rows affected since the database connection was opened: ", self.sqliteConnection.total_changes)
            # self.sqliteConnection.close()
            print("sqlite connection is closed")

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def select_fp_attendance_record(self, fp_id, cur_date):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            cursor.execute("""SELECT checkin_time FROM fp_att WHERE (fp_id, cur_date) in (values(?, ?))""",
                           (fp_id, cur_date))
            row = cursor.fetchone()
            print("get it 0", row)
            # for row in rows:
            #     print(row)

            # self.sqliteConnection.commit()
            cursor.close()
            return row

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def select_fp_attendance_status(self, fp_id, cur_date):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            cursor.execute(
                """SELECT status, exit_status FROM fp_att WHERE (fp_id, cur_date) in (values(?, ?))""",
                (fp_id, cur_date))
            row = cursor.fetchone()
            print("get it ", row)
            # for all in row:
            #     status1 = all[0]
            #     status2 = all[1]

            # self.sqliteConnection.commit()
            cursor.close()
            return row

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def select_fp_attendance_all_record(self):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            rows = cursor.execute("""SELECT * FROM fp_att""")
            # row = cursor.fetchone()
            for row in rows:
                print(row)

            # self.sqliteConnection.commit()
            cursor.close()
            return rows

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def update_attendance_status(self, checkin_status, fp_id, cur_date):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            cursor.execute("""UPDATE fp_att SET status = ? WHERE (fp_id, cur_date) in (values(?, ?))""",
                           (checkin_status, fp_id, cur_date))
            row = cursor.fetchone()
            # for row in rows:
            #     print(row)

            self.sqliteConnection.commit()
            cursor.close()
            return row

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

    def update_checkout_status(self, checkout_status, fp_id, cur_date):
        try:
            # sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = self.sqliteConnection.cursor()
            print("Connected to SQLite")

            cursor.execute(
                """UPDATE fp_att SET exit_status = ?, checkout_time = ? WHERE (fp_id, cur_date) in (values(?, ?))""",
                (checkout_status, datetime.datetime.now(), fp_id, cur_date))
            # row = cursor.fetchone()
            # for row in rows:
            #     print(row)

            self.sqliteConnection.commit()
            cursor.close()
            # return row

        except sqlite3.Error as error:
            print("Error while working with SQLite", error)

# att = FPAttendanceSystemDB()
# att.insert_data('AR', datetime.datetime.now(), 1)
# att.select_registered_fp(1)
# att.select_registered_fp(2)
# att.select_registered_fp(3)
# att.select_registered_fp(4)
# att.create_db_table()

# att.select_fp_attendance_All_record()
# att.insert_attendance('Rehman', datetime.date.today(), datetime.datetime.now(), 1)
# att.select_fp_attendance_All_record()

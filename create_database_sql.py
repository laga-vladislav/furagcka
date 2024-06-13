import os
import sqlite3
import config


def create_database(filename):
    """ create a database connection to an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
        create_tables(conn)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def execute_stmt(conn, sql_stmts: list[str]):
    try:
        cursor = conn.cursor()
        for statement in sql_stmts:
            cursor.execute(statement)

        conn.commit()
    except sqlite3.Error as e:
        print(e)


def drop_tables(conn):
    stmts = ["DROP TABLE user", "DROP TABLE note"]
    execute_stmt(conn, stmts)


def create_tables(conn):
    stmts = [
        """CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY, 
                login TEXT NOT NULL, 
                password BLOB NOT NULL
        );""",
        """CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                header TEXT NOT NULL, 
                file BLOB NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user (id)
        );"""]
    execute_stmt(conn, stmts)


def delete_database(filename):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        drop_tables(conn)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    delete_database(config.DB_NAME)
    create_database(config.DB_NAME)

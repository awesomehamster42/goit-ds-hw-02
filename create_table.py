from sqlite3 import Error
from connect import create_connection, database


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)


def insert_data(conn, insert_sql, values=None):
    try:
        c = conn.cursor()
        if values:
            c.executemany(insert_sql, values)
        else:
            c.execute(insert_sql)
        conn.commit()
    except Error as e:
        print(e)


if __name__ == "__main__":
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname  VARCHAR(100) NOT NULL,
        email     VARCHAR(100) NOT NULL UNIQUE
    );
    """

    sql_create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
        id    INTEGER PRIMARY KEY AUTOINCREMENT,
        name  VARCHAR(50) NOT NULL UNIQUE
    );
    """

    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        title       VARCHAR(100) NOT NULL,
        description TEXT,
        status_id   INTEGER NOT NULL,
        user_id     INTEGER NOT NULL,
        FOREIGN KEY (status_id) REFERENCES status(id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
        FOREIGN KEY (user_id) REFERENCES users(id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );
    """

    sql_insert_status = """
    INSERT OR IGNORE INTO status (name) VALUES (?);
    """

    # Дані для вставки
    status_values = [
        ("new",),
        ("in progress",),
        ("completed",)
    ]

    with create_connection(database) as conn:
        if conn is not None:
            # створення таблиць
            create_table(conn, sql_create_users_table)
            create_table(conn, sql_create_status_table)
            create_table(conn, sql_create_tasks_table)

            # заповнення таблиці статусів
            insert_data(conn, sql_insert_status, status_values)

        else:
            print("Error! cannot create the database connection.")

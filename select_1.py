from sqlite3 import Error
from connect import create_connection, database

def select_tasks_by_user(conn, user_id):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_tasks_by_status(conn, status_name):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("""
        SELECT * FROM tasks WHERE status_id IN (SELECT id FROM status WHERE name=?);
        """, (status_name,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def update_task_status(conn, task_id, new_status):
    cur = conn.cursor()
    try:
        cur.execute("""
        UPDATE tasks
        SET status_id = (SELECT id FROM status WHERE name=?)
        WHERE id=?;
        """, (new_status, task_id))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


def select_users_without_tasks(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("""
        SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);
        """)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def insert_new_task(conn, title, description, status_name, user_id):
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (?, ?, (SELECT id FROM status WHERE name=?), ?);
        """, (title, description, status_name, user_id))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


def select_incomplete_tasks(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("""
        SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name='completed');
        """)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def delete_task(conn, task_id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


def select_users_by_email(conn, email_pattern):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email LIKE ?", (email_pattern,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def update_user_name(conn, user_id, new_name):
    cur = conn.cursor()
    try:
        cur.execute("UPDATE users SET fullname=? WHERE id=?", (new_name, user_id))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        cur.close()


def count_tasks_by_status(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("""
        SELECT status.name, COUNT(tasks.id) 
        FROM tasks
        JOIN status ON tasks.status_id = status.id
        GROUP BY status.name;
        """)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_tasks_by_user_email_domain(conn, domain):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("""
        SELECT tasks.* 
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE users.email LIKE ?;
        """, ('%' + domain,))
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_tasks_without_description(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM tasks WHERE description IS NULL OR description='';")
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_users_in_progress_tasks(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("""
        SELECT users.fullname, tasks.title 
        FROM users
        INNER JOIN tasks ON users.id = tasks.user_id
        JOIN status ON tasks.status_id = status.id
        WHERE status.name = 'in progress';
        """)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows


def select_users_and_task_count(conn):
    rows = None
    cur = conn.cursor()
    try:
        cur.execute("""
        SELECT users.fullname, COUNT(tasks.id) 
        FROM users
        LEFT JOIN tasks ON users.id = tasks.user_id
        GROUP BY users.id;
        """)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        cur.close()
    return rows
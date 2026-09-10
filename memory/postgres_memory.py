# import psycopg2
# from config.settings import settings
#
#
# def get_connection():
#     return psycopg2.connect(
#         host=settings.POSTGRES_HOST,
#         port=settings.POSTGRES_PORT,
#         dbname=settings.POSTGRES_DB,
#         user=settings.POSTGRES_USER,
#         password=settings.POSTGRES_PASSWORD
#     )
#
#
# def save_fact(session_id: str, fact: str, user_id: str = None):
#     user_id = user_id or session_id
#     conn = get_connection()
#     cur = conn.cursor()
#
#     cur.execute(
#         "INSERT INTO facts (user_id, session_id, fact) VALUES (%s, %s, %s)",
#         (user_id, session_id, fact)
#     )
#
#     conn.commit()
#     cur.close()
#     conn.close()
#
#
# def get_facts(session_id: str, user_id: str = None) -> list:
#     user_id = user_id or session_id
#     conn = get_connection()
#     cur = conn.cursor()
#
#     cur.execute(
#         "SELECT fact FROM facts WHERE user_id = %s ORDER BY created_at",
#         (user_id,)
#     )
#
#     rows = cur.fetchall()
#     cur.close()
#     conn.close()
#
#     return [row[0] for row in rows]
#
#
# def clear_facts(session_id: str, user_id: str = None):
#     user_id = user_id or session_id
#     conn = get_connection()
#     cur = conn.cursor()
#
#     cur.execute("DELETE FROM facts WHERE user_id = %s", (user_id,))
#
#     conn.commit()
#     cur.close()
#     conn.close()

import psycopg2
from config.settings import settings

def get_connection():
    return psycopg2.connect(
        host = settings.POSTGRES_HOST,
        port = settings.POSTGRES_PORT,
        dbname = settings.POSTGRES_DB,
        user = settings.POSTGRES_USER,
        password = settings.POSTGRES_PASSWORD
    )

def save_fact(session_id: str , fact:str , user_id : str = None):
    user_id = user_id or session_id
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO facts(user_id , session_id , fact) VALUES (%s,%s, %s)",
        (user_id , session_id , fact)
    )

    conn.commit()
    cur.close()
    conn.close()

def get_facts(session_id : str , user_id : str = None) -> list :
    user_id = user_id or session_id
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT fact FROM facts where user_id = %s ORDER BY created_at",
        (user_id,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()
    return [row[0] for row in rows]

def clear_facts(session_id: str , user_id : str = None):
    user_id = user_id or session_id
    conn = get_connection()
    cur = conn. cursor()

    cur.execute(
        "DELETE FROM facts WHERE user_id = %s ",(user_id,)
    )
    conn.commit()
    cur.close()
    conn.close()

def init_user_table():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                name VARCHAR(255),
                picture TEXT,
                auth_provider VARCHAR(50) DEFAULT 'local',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        # Ensure facts table is initialized
        cur.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                session_id VARCHAR(255) NOT NULL,
                fact TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Postgres tables initialized successfully.")
    except Exception as e:
        print(f"Error initializing Postgres user/facts tables: {e}")

def create_local_user(email: str, password_hash: str, name: str) -> dict:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password_hash, name, auth_provider) VALUES (%s, %s, %s, 'local') RETURNING id, email, name, picture, auth_provider",
        (email, password_hash, name)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {
        "id": row[0],
        "email": row[1],
        "name": row[2],
        "picture": row[3],
        "auth_provider": row[4]
    }

def get_user_by_email(email: str) -> dict:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, password_hash, name, picture, auth_provider FROM users WHERE email = %s",
        (email,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "email": row[1],
        "password_hash": row[2],
        "name": row[3],
        "picture": row[4],
        "auth_provider": row[5]
    }

def get_or_create_google_user(email: str, name: str, picture: str) -> dict:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, email, name, picture, auth_provider FROM users WHERE email = %s", (email,))
    row = cur.fetchone()
    if row:
        cur.execute(
            "UPDATE users SET name = %s, picture = %s WHERE email = %s RETURNING id, email, name, picture, auth_provider",
            (name, picture, email)
        )
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {
            "id": row[0],
            "email": row[1],
            "name": row[2],
            "picture": row[3],
            "auth_provider": row[4]
        }
    else:
        cur.execute(
            "INSERT INTO users (email, name, picture, auth_provider) VALUES (%s, %s, %s, 'google') RETURNING id, email, name, picture, auth_provider",
            (email, name, picture)
        )
        row = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {
            "id": row[0],
            "email": row[1],
            "name": row[2],
            "picture": row[3],
            "auth_provider": row[4]
        }
import sqlite3
import os
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "system.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS students")
    cursor.execute("DROP TABLE IF EXISTS users")

    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        roll_no TEXT UNIQUE,
        attendance REAL,
        study_hours REAL,
        assignment_score REAL,
        mid_exam_score REAL,
        previous_sem_score REAL,
        participation_score REAL,
        risk_level TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_default_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
    """, ("Admin User", "admin@gmail.com",
          hash_password("admin123"), "admin"))

    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
    """, ("Faculty User", "faculty@gmail.com",
          hash_password("faculty123"), "faculty"))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    insert_default_users()
    print("Database created successfully.")

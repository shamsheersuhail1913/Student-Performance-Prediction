import psycopg2
import hashlib
import streamlit as st


def get_connection():
    return psycopg2.connect(st.secrets["DATABASE_URL"])


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
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

    # Insert default users if not exist
    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (email) DO NOTHING
    """, ("Admin User", "admin@gmail.com", hash_password("admin123"), "admin"))

    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (email) DO NOTHING
    """, ("Faculty User", "faculty@gmail.com", hash_password("faculty123"), "faculty"))

    conn.commit()
    conn.close()

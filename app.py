import streamlit as st
import psycopg2
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import os
import hashlib
from database import create_tables

# ---------- LOAD MODEL ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_data = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
model = model_data["model"]
FEATURE_COLUMNS = model_data["features"]

# ---------- CONFIG ----------
st.set_page_config(page_title="Student Performance System", layout="wide")

# ---------- STYLING ----------
st.markdown("""
<style>
body {background: linear-gradient(to right, #141e30, #243b55);}
.stMetric {background-color:#ffffff15;padding:15px;border-radius:12px;}
div.stButton > button {background-color:#00c6ff;color:white;border-radius:8px;}
div.stButton > button:hover {background-color:#0072ff;transform:scale(1.05);}
</style>
""", unsafe_allow_html=True)

# ---------- INIT DB ----------
create_tables()

# ---------- HELPERS ----------
def get_connection():
    return psycopg2.connect(st.secrets["DATABASE_URL"])

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

# ---------- LOGIN ----------
if not st.session_state.logged_in:

    st.title("🎓 Student Performance Prediction System")

    username = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (username, hash_password(password))
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            st.session_state.logged_in = True
            st.session_state.role = user[4]
            st.session_state.username = user[2]
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------- DASHBOARD ----------
else:

    role = st.session_state.role
    username = st.session_state.username

    st.sidebar.write(f"Logged in as: {username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # ================= ADMIN =================
    if role == "admin":

        st.header("🛡 Admin Dashboard")

        conn = get_connection()
        df = pd.read_sql("SELECT * FROM students", conn)
        conn.close()

        if not df.empty:

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Students", len(df))
            col2.metric("High Risk", len(df[df["risk_level"]=="High"]))
            col3.metric("Low Risk", len(df[df["risk_level"]=="Low"]))

            risk_counts = df["risk_level"].value_counts().reset_index()
            risk_counts.columns = ["Risk Level", "Count"]

            fig = px.pie(risk_counts,
                         names="Risk Level",
                         values="Count",
                         color="Risk Level",
                         color_discrete_map={
                             "High":"red",
                             "Medium":"orange",
                             "Low":"green"
                         })
            st.plotly_chart(fig)

            st.subheader("Feature Importance")
            importance = model.feature_importances_
            fig2 = px.bar(x=importance, y=FEATURE_COLUMNS, orientation='h')
            st.plotly_chart(fig2)

        else:
            st.info("No student records yet.")

    # ================= FACULTY =================
    elif role == "faculty":

        st.header("👨🏫 Faculty Dashboard")

        st.subheader("➕ Add Student")

        if "clear_trigger" not in st.session_state:
            st.session_state.clear_trigger = False

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Student Name", key="name")
            roll = st.text_input("Roll Number", key="roll")
            attendance = st.number_input("Attendance", 0.0, 100.0, key="attendance")
            study = st.number_input("Study Hours", key="study")

        with col2:
            assign = st.number_input("Assignment Score", 0.0, 100.0, key="assign")
            mid = st.number_input("Mid Exam Score", 0.0, 100.0, key="mid")
            prev = st.number_input("Previous Sem Score", 0.0, 100.0, key="prev")
            part = st.number_input("Participation Score", 0.0, 10.0, key="part")

        btn1, btn2 = st.columns(2)

        if btn1.button("Predict & Save"):

            input_data = np.array([[attendance, study, assign, mid, prev, part]])
            prediction = model.predict(input_data)[0]

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO students
                (student_name, roll_no, attendance, study_hours,
                assignment_score, mid_exam_score,
                previous_sem_score, participation_score, risk_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, roll, attendance, study, assign, mid, prev, part, prediction))

            cursor.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, 'student')
                ON CONFLICT (email) DO NOTHING
            """, (name, roll, hash_password("Student123")))

            conn.commit()
            conn.close()

            st.success("Student Saved Successfully")

            for key in ["name","roll","attendance","study","assign","mid","prev","part"]:
                st.session_state[key] = ""
            st.rerun()

        if btn2.button("Clear"):
            for key in ["name","roll","attendance","study","assign","mid","prev","part"]:
                st.session_state[key] = ""
            st.rerun()

        st.markdown("---")
        st.subheader("📋 Student Records")

        conn = get_connection()
        df = pd.read_sql("SELECT * FROM students", conn)
        conn.close()

        if not df.empty:

            st.dataframe(df, use_container_width=True)

            st.markdown("---")
            st.subheader("✏ Edit / Delete Student")

            selected_id = st.selectbox("Select Student ID", df["id"])
            student = df[df["id"] == selected_id].iloc[0]

            colA, colB = st.columns(2)

            with colA:
                new_name = st.text_input("Name", student["student_name"])
                new_roll = st.text_input("Roll No", student["roll_no"])
                new_att = st.number_input("Attendance", 0.0, 100.0, float(student["attendance"]))
                new_study = st.number_input("Study Hours", value=float(student["study_hours"]))
                new_assign = st.number_input("Assignment", 0.0, 100.0, float(student["assignment_score"]))

            with colB:
                new_mid = st.number_input("Mid Exam", 0.0, 100.0, float(student["mid_exam_score"]))
                new_prev = st.number_input("Previous Sem", 0.0, 100.0, float(student["previous_sem_score"]))
                new_part = st.number_input("Participation", 0.0, 10.0, float(student["participation_score"]))

            col_update, col_delete = st.columns(2)

            if col_update.button("Update Student"):

                input_data = np.array([[new_att, new_study, new_assign, new_mid, new_prev, new_part]])
                prediction = model.predict(input_data)[0]

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE students
                    SET student_name=%s, roll_no=%s, attendance=%s, study_hours=%s,
                        assignment_score=%s, mid_exam_score=%s,
                        previous_sem_score=%s, participation_score=%s, risk_level=%s
                    WHERE id=%s
                """, (new_name, new_roll, new_att, new_study,
                      new_assign, new_mid, new_prev, new_part, prediction, selected_id))
                conn.commit()
                conn.close()

                st.success("Student Updated Successfully")
                st.rerun()

            if col_delete.button("Delete Student"):

                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE id=%s", (selected_id,))
                cursor.execute("DELETE FROM users WHERE email=%s", (student["roll_no"],))
                conn.commit()
                conn.close()

                st.warning("Student Deleted Successfully")
                st.rerun()

        else:
            st.info("No students available.")

    # ================= STUDENT =================
    elif role == "student":

        st.header("🎓 Student Dashboard")

        conn = get_connection()
        df = pd.read_sql("SELECT * FROM students WHERE roll_no=%s",
                         conn, params=(username,))
        conn.close()

        if not df.empty:

            student = df.iloc[0]

            st.success(f"Welcome {student['student_name']}")

            col1, col2, col3 = st.columns(3)
            col1.metric("Attendance", f"{student['attendance']}%")
            col2.metric("Study Hours", student["study_hours"])
            col3.metric("Assignment Score", student["assignment_score"])

            col4, col5, col6 = st.columns(3)
            col4.metric("Mid Exam", student["mid_exam_score"])
            col5.metric("Previous Sem", student["previous_sem_score"])
            col6.metric("Participation", student["participation_score"])

            st.subheader("📈 Academic Trend")
            trend_data = [
                student["assignment_score"],
                student["mid_exam_score"],
                student["previous_sem_score"]
            ]
            st.line_chart(trend_data)

            st.subheader("📊 Risk Level")
            risk = student["risk_level"]

            if risk == "High":
                st.error("🔴 High Risk Level")
                st.markdown("""
                ### Immediate Action Plan:
                - Increase study hours to at least 3–4 hours daily
                - Improve attendance above 75%
                - Focus on weak subjects
                - Revise previous semester fundamentals
                - Practice mock tests weekly
                """)
                st.warning("You can turn this around. Consistency matters more than intensity.")

            elif risk == "Medium":
                st.warning("🟡 Medium Risk Level")
                st.markdown("""
                ### Keep Improving:
                - Maintain daily study schedule
                - Improve assignment quality
                - Increase classroom participation
                - Revise topics before exams
                """)
                st.info("You're close to Low Risk. Small improvements will make a big difference.")

            else:
                st.success("🟢 Low Risk Level")
                st.markdown("""
                ### Performance Boost Plan:
                - Try advanced practice problems
                - Participate in competitions
                - Help peers to strengthen concepts
                - Start working on real-world projects
                """)
                st.info("Excellent performance. Now focus on mastering concepts deeply.")

        else:
            st.error("No academic record found.")

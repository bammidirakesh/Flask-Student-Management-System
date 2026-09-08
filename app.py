from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# -----------------------------------------
# CREATE DATABASE TABLE
# -----------------------------------------

def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# -----------------------------------------
# HOME PAGE - DISPLAY ALL STUDENTS
# GET REQUEST
# -----------------------------------------

@app.route("/")
def index():

    connection = get_db_connection()

    students = connection.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template(
        "index.html",
        students=students
    )


# -----------------------------------------
# ADD STUDENT
# GET + POST REQUEST
# -----------------------------------------

@app.route("/add", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]

        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO students
            (name, email, department)
            VALUES (?, ?, ?)
            """,
            (name, email, department)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    return render_template("add_student.html")


# -----------------------------------------
# EDIT STUDENT
# GET + POST REQUEST
# -----------------------------------------

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    connection = get_db_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]

        connection.execute(
            """
            UPDATE students
            SET name = ?, email = ?, department = ?
            WHERE id = ?
            """,
            (name, email, department, student_id)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    connection.close()

    return render_template(
        "edit_student.html",
        student=student
    )


# -----------------------------------------
# DELETE STUDENT
# -----------------------------------------

@app.route("/delete/<int:student_id>")
def delete_student(student_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("index"))


# -----------------------------------------
# RUN APPLICATION
# -----------------------------------------

if __name__ == "__main__":

    create_table()

    app.run(debug=True)
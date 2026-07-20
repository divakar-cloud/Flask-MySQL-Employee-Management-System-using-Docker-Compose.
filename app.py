from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

@app.route("/")
def home():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees")

    employees = cursor.fetchall()

    conn.close()

    return render_template("index.html", employees=employees)


@app.route("/add", methods=["POST"])

def add_employee():

    name = request.form["name"]

    role = request.form["role"]

    department = request.form["department"]

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO employees(name,role,department) VALUES(%s,%s,%s)",
        (name, role, department)
    )

    conn.commit()

    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
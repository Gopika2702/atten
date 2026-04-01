from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database connection (XAMPP MySQL)
import random
import os
from urllib.parse import urlparse
 
app = Flask(__name__)
 
# 🔥 GET DATABASE URL
db_url = os.getenv("mysql://root:jMcOhuklihFQMHMfdWPnoDoBCKGYfwXh@interchange.proxy.rlwy.net:29246/railway")
 
# 👉 fallback for local testing (IMPORTANT)
if not db_url:
    db_url = "mysql://root:jMcOhuklihFQMHMfdWPnoDoBCKGYfwXh@interchange.proxy.rlwy.net:29246/railway"
 
url = urlparse(db_url)
 
# 🔥 DATABASE CONNECTION
db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # ✅ correct way (remove "/")
    port=url.port
)
 
cursor = db.cursor()
cursor = db.cursor(dictionary=True)

# READ - Display all records
@app.route('/')
def index():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('index.html', students=students, student=None)

# CREATE - Add new student attendance
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    roll = request.form['roll']
    status = request.form['status']
    date = request.form['date']   # user selects date
    cursor.execute("INSERT INTO students (name, roll, status, date) VALUES (%s, %s, %s, %s)",
                   (name, roll, status, date))
    db.commit()
    return redirect('/')

# UPDATE - Edit attendance
@app.route('/update/<roll>', methods=['GET', 'POST'])
def update(roll):
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        date = request.form['date']
        cursor.execute("UPDATE students SET name=%s, status=%s, date=%s WHERE roll=%s",
                       (name, status, date, roll))
        db.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM students WHERE roll=%s", (roll,))
    student = cursor.fetchone()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('index.html', students=students, student=student)

# DELETE - Remove student record
@app.route('/delete/<roll>')
def delete(roll):
    cursor.execute("DELETE FROM students WHERE roll=%s", (roll,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

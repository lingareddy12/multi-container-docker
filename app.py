from flask import Flask,render_template,request,redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)



# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='db',
            user='root',
            password='rootpassword',
            database='testdb'
        )
    except Error as e:
        pass
    return connection 

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    create_table_query = """CREATE TABLE IF NOT EXISTS students (name VARCHAR(255) NOT NULL,roll_no INT NOT NULL PRIMARY KEY,marks FLOAT)"""
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()
    
    

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/Add-Student',methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form['name']
        roll=request.form['roll_no']
        marks=request.form['marks']
        
        create_table()
        
        connection=create_connection()
        cursor = connection.cursor()
        query = "INSERT INTO students (name, roll_no, marks) VALUES (%s, %s, %s)"
        values = (name, roll, marks)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    return render_template("add_student.html")

@app.route('/Display-Students-Data')
def students():
    connection=create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    student_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('students.html', students=student_data)


@app.route('/home')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    create_table()
    app.run(debug=True, host="0.0.0.0")

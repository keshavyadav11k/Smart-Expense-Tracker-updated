from flask import Flask,render_template,request
import mysql.connector

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():


    return render_template('register.html')

@app.route('/perform_registration',methods = ['POST'])
def perform_registration():
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="set"
    )

        cursor = connection.cursor()

    # Example: user_id is DOUBLE
        insert_query = "INSERT INTO users (name, username, email, password) VALUES ( %s,%s, %s, %s)"
    
    # Data to insert
        data = (name, username, email,password)  # user_id as float

        cursor.execute(insert_query, data)
        connection.commit()

        print("Record inserted successfully!")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)

    finally:    
     if connection.is_connected():
        cursor.close()
        connection.close()

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
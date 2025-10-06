from flask import Flask,render_template,request
# import mysql.connector
import db 
app = Flask(__name__)



@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():


    return render_template('register.html')

@app.route('/perform_registration',methods = ['POST'])
def perform_registration():
    mydatabase = db.MyDatabase()
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    result  =  mydatabase.insertUserData(name,username,email,password)
    print("value of result is ",result)
    if result == 1:
        
        return render_template('login.html')
        # return f"user registered successfully , {result}"
    else:
        return f"user already present , {result}"

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask,render_template,request,redirect,session,url_for
# import mysql.connector
import db 
app = Flask(__name__)
# IMPORTANT: Sessions require a secret key to sign the cookies. 
# Change this to a long, complex, random value in a real application.
app.secret_key = 'your_super_secure_secret_key_12345' 


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('user_dashboard'))
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
        
        return render_template('login.html',message='Account created successfully! Please log in to continue.',
        message_type='success'                       )
        # return f"user registered successfully , {result}"
    else:
        return render_template('register.html',message='This username is already taken. Kindly choose another.',
        message_type='error')
        # return f"user already present , {result}"
    
@app.route("/perform_login",methods = ['POST'])
def perform_login():

    mydatabase = db.MyDatabase()
    username = request.form.get("username")
    password = request.form.get("password")
    result  = mydatabase.loginUser(username,password)
    if result ==1:
        # STEP 1: Store the successful username in the Flask session
        session['username'] = username
        # session['name'] = 
        return redirect(url_for('user_dashboard'))
    else:
        # return f"invalid username or password {result}"
        return render_template('login.html',message='Invalid username or password.',
        message_type='error')
    
@app.route('/dashboard')
def user_dashboard():
    # STEP 2: Retrieve the username from the session
    username = session.get('username')
    name  = 'Keshav'
     # Basic security check: if no username in session, redirect to login

    if not username:
        return redirect('/')
    else:
        mydatabase = db.MyDatabase()
        response = mydatabase.get_user_analysis(username)
        amount_total_spent = response[0]
        expense_count  =  response[1]
        budget = response[2]
        total_budget = response[3]



    # STEP 3: Pass the username to the template using render_template
    return render_template('dashboard.html', username=username,amount_total_spent=amount_total_spent,expense_count=expense_count,budget=budget,total_budget=total_budget)

@app.route('/profile')
def user_profile():

    username = session.get('username')
    mydatabase = db.MyDatabase()
    response = mydatabase.get_user_details(username)
    # print("hello username : ",response)
    logged_in_name = response[0]
    logged_in_email = response[1]
    logged_in_username = response[2]
    return render_template('profile.html',name=logged_in_name,email=logged_in_email,username=logged_in_username)

@app.route('/add_expense')
def add_expense():
    # mydatabase = db.MyDatabase()

    # mydatabase.add_user_expense()
    return render_template('add_expense.html')

@app.route('/perform_add_expense',methods=['POST'])
def perform_add_expense():
    amount = request.form.get('amount')
    category = request.form.get('category')
    date = request.form.get('date')
    description = request.form.get('description')
    username = session.get('username')


    mydatabase = db.MyDatabase()
    print('flask insert details of expense',amount,category,description,date,username)
    mydatabase.add_user_expense(amount,category,description,date,username)

    return render_template('add_expense.html',message='Expense added successfully',
                           message_type='success')



@app.route('/add_budget')
def add_budget():
    # mydatabase = db.MyDatabase()

    # mydatabase.add_user_expense()
    return render_template('add_budget.html')

@app.route('/perform_add_budget',methods=['POST'])
def perform_add_budget():
    amount = request.form.get('amount')
    
    username = session.get('username')


    mydatabase = db.MyDatabase()
    print('flask insert details of expense',amount,username)
    mydatabase.add_user_budget(amount,username)

    return render_template('add_budget.html',message='Budget added successfully',
                           message_type='success')

@app.route('/logout')
def logout():
    # Clear the session data to log the user out
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

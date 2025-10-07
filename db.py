import mysql.connector

class MyDatabase: 
    def __init__(self):
        self.__username = ""
        self.flag = 1
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="set")
            self.cursor = self.connection.cursor()
        
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
       

    def insertUserData(self,name,username,email,password):
        try:

            self.__username = username
            # flag = 1
            result  = self.checkduplicateuser(self.__username)
            if result == 1:
                
                insert_query = "INSERT INTO users (name, username, email, password) VALUES ( %s,%s, %s, %s)"
    
                # Data to insert
                data = (name, username, email,password)  # user_id as float

                self.cursor.execute(insert_query, data)
                self.connection.commit()

                print("Record inserted successfully!")
                return self.flag

            else:
                print("username already present")
                self.flag = 0
                return self.flag

        except mysql.connector.Error as err:
            print("MySQL Error:", err)

        finally:    
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
        
        
        
    def checkduplicateuser(self,username):
        self.check  = 1
        try:
            # SQL SELECT query
            select_query = "SELECT username FROM users"

            self.cursor.execute(select_query)

            # Fetch all rows
            rows = self.cursor.fetchall()
             # print("user in rows",rows)
            available_username = [row[0] for row in rows]
            print(available_username)
            if username  in available_username:
                self.check = 0

        except mysql.connector.Error as err:
            print("MySQL Error:", err)
        return self.check

    def loginUser(self,username,password):
        check = 1
        try:
            # SQL SELECT query
            select_query = f'SELECT password FROM users where username = "{username}"'
            # print(select_query)
            self.cursor.execute(select_query)

            # Fetch all rows
            rows = self.cursor.fetchall()
            if rows:
                # print(rows)
                db_pass = [row[0] for row in rows]
                # print(db_pass)
                if password  in db_pass:
                    return check
                else:
                    check = 0
                    return check 
            else:
                print("no record found")
             # print("user in rows",rows)
                check = 0
                return check
            
            

        except mysql.connector.Error as err:
            print("MySQL Error:", err)
        finally:    
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
    
    def get_user_details(self,username):

        try:
            # SQL SELECT query
            select_query = f'SELECT name,email,username FROM users where username = "{username}"'
            # print(select_query)
            self.cursor.execute(select_query)

            # Fetch all rows
            rows = self.cursor.fetchall()
            # if rows:
                # print("details of current user is : ",rows)
                # db_pass = [row[0] for row in rows]
                # print(db_pass)
                # return check 
            logged_in_name  = rows[0][0]
            logged_in_email = rows[0][1]
            logged_in_username  = rows[0][2]
            # print(logged_in_name,logged_in_email,logged_in_username)
            return logged_in_name,logged_in_email,logged_in_username
            
            

        except mysql.connector.Error as err:
            print("MySQL Error:", err)
        finally:    
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
    

    
    def add_user_expense(self,amount,category,description,date,username):
        try:

            # flag = 1
            # result  = self.checkduplicateuser(self.__username)
            # if result == 1:
                insert_query = "INSERT INTO expenses (amount,category,description,date,username) VALUES (%s, %s,%s, %s, %s)"
                # Data to insert
                amount = amount
                category = category
                description = description
                date = date
                username = username
                # print('db insert details of expense',amount,category,description,date,username)
                data = (amount,category,description,date,username)  # user_id as float

                self.cursor.execute(insert_query, data)
                self.connection.commit()

                print("Record inserted successfully!")
                # return self.flag


        except mysql.connector.Error as err:
            print("MySQL Error:", err)

        finally:    
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
    
    def get_user_analysis(self,username):

        try:
            # SQL SELECT query
            # select_query = f'SELECT name,email,username FROM users where username = "{username}"'
            select_query = f'SELECT sum(amount) FROM expenses where username = "{username}"  AND MONTH(date) = MONTH(CURRENT_DATE()) AND YEAR(date) = YEAR(CURRENT_DATE())'
            # print(select_query)
            self.cursor.execute(select_query)
            rows = self.cursor.fetchone()
            # print('row data and type of row  ',rows,type(rows))
            # print('type of row data',rows[0])
            if rows[0] == None:
                amount_total_spent = 0
            else:
             amount_total_spent  = float(rows[0])
            # print("amount is :",amount)

            select_query = f'SELECT count(*) FROM expenses where username = "{username}"  AND MONTH(date) = MONTH(CURRENT_DATE()) AND YEAR(date) = YEAR(CURRENT_DATE())'
            # print(select_query)
            self.cursor.execute(select_query)
            rows = self.cursor.fetchone()
            # expense_count  = float(rows[0])
            # print('expense count is :',rows[0])
            expense_count  = rows[0]

            select_query = f'''select (SELECT budget_amount FROM budget WHERE USERNAME = "{username}"
            AND MONTH(budget_month) = MONTH(CURRENT_DATE()) AND YEAR(budget_month) = YEAR(CURRENT_DATE()))-
            (SELECT sum(amount) FROM expenses where username ="{username}"
            AND MONTH(date) = MONTH(CURRENT_DATE()) AND YEAR(date) = YEAR(CURRENT_DATE())) AS result FROM DUAL'''

            # print(select_query)
            self.cursor.execute(select_query)
            rows = self.cursor.fetchone()
            # print('row data and type of row  ',rows,type(rows))
            # print('type of row data',rows[0])
            if rows[0] == None:
                budget = 0
            else:
                budget  = rows[0]
            # print(budget)

            select_query = f'''SELECT budget_amount FROM budget WHERE USERNAME = "{username}"
            AND MONTH(budget_month) = MONTH(CURRENT_DATE()) AND YEAR(budget_month) = YEAR(CURRENT_DATE())'''

            # print(select_query)
            self.cursor.execute(select_query)
            rows = self.cursor.fetchone()
            # print('row and type of row',rows,type(rows))
            # print()
            if rows == None:
                total_budget = 0
            else:
                total_budget  = rows[0]
            # print("total_budget is : ",total_budget)



            return amount_total_spent,expense_count,budget,total_budget
            
            

        except mysql.connector.Error as err:
            print("MySQL Error:", err)
        finally:    
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
    

    def add_user_budget(self,amount,username):
        try:

            # flag = 1
            # result  = self.checkduplicateuser(self.__username)
            # if result == 1:
                insert_query = "INSERT INTO budget (budget_amount,username) VALUES (%s, %s)"
                # Data to insert
                amount = amount
                username = username
                # print('db insert details of expense',amount,username)
                data = (amount,username) 

                self.cursor.execute(insert_query, data)
                self.connection.commit()

                print("Record inserted successfully!")
                # return self.flag


        except mysql.connector.Error as err:
            print("MySQL Error:", err)

        finally:    
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
    
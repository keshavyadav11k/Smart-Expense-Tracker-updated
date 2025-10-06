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
                # Example: user_id is DOUBLE
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


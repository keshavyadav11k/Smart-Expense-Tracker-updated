import mysql.connector

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="set"
    )

    cursor = connection.cursor()

    # SQL SELECT query
    select_query = "SELECT username FROM users"

    cursor.execute(select_query)

    # Fetch all rows
    rows = cursor.fetchall()
    # print("user in rows",rows)
    available_username = [row[0] for row in rows]
    print(available_username)
    # if rows:
    #     print(" Users in database:")
    #     for row in rows:
    #         print(row)
    # else:
    #     print("No records found.")

except mysql.connector.Error as err:
    print("MySQL Error:", err)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
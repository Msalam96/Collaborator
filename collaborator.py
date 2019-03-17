import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", passwd="password", database="collaboratordb")

c = conn.cursor(buffered=True)

c.execute("CREATE DATABASE IF NOT EXISTS collaboratordb")

c.execute("""CREATE TABLE IF NOT EXISTS user (
        user_id int AUTO_INCREMENT PRIMARY KEY,
        first text,
        last text,
        phone text,
        address text,
        degree text 
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS interest (
        user_id int PRIMARY KEY,
        interest text,
        interest_level integer
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS distance (
        org1 text,
        org2 text,
        distance real
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS organization (
        user_id integer AUTO_INCREMENT PRIMARY KEY,
        org_name text,
        org_type text
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS project (
        user_id integer AUTO_INCREMENT PRIMARY KEY,
        proj_name text
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS skill (
        user_id integer AUTO_INCREMENT PRIMARY KEY, 
        skill_name text,
        skill_level integer
        )""")

print("Welcome to the Collaborator Software. Here are the following inputs:")


x = c.execute("SELECT MAX(user_id) FROM user")
print(x)

while True:
    key = input(""" 
Press 1 if you wish to add a user to our database.
Press 2 to print users
Press 0 to exit \n-> """)
    if key == '1':
        first = input("What is your first name?\n-> ")
        last = input("What is your last name?\n-> ")
        phone = input("What is your phone number?\n-> ")
        address = input("What is your address?\n-> ")
        degree = input("What degree did you earn?\n-> ")
        c.execute("INSERT INTO user VALUES (%s,%s,%s, %s, %s, %s)", (x, first, last, phone, address, degree))
        x += 1
        conn.commit()
    elif key == '2':
        cur = conn.cursor()
        cur.execute("SELECT * FROM user")
        rows = cur.fetchall()
        print(rows)
    elif key == '0':
        print("Thank you for using our software")
        break
    else:
        print("This input was not recognized.")

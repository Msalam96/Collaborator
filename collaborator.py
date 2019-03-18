import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", passwd="password", database="collaboratordb")

c = conn.cursor(buffered=True)

c.execute("CREATE DATABASE IF NOT EXISTS collaboratordb")

c.execute("""CREATE TABLE IF NOT EXISTS user (
        user_id integer AUTO_INCREMENT PRIMARY KEY,
        first text,
        last text,
        phone text,
        address text,
        degree text 
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS interest (
        user_id integer PRIMARY KEY,
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


x = 0

while True:
    key = input(""" 
Press 1 to add a user to our database.
Press 2 to find information about a specific user. 
Press 0 to exit \n-> """)
    if key == '1':
        first = input("What is your first name?\n-> ")
        last = input("What is your last name?\n-> ")
        phone = input("What is your phone number?\n-> ")
        address = input("What is your address?\n-> ")
        degree = input("What degree did you earn?\n-> ")
        org = input("What organization do you work at?\n-> ")
        orgtype = input("What type of organization is this?\n-> ")
        project = input("List a project a you have worked on:\n-> ")
        interest = input("List an interest you have:\n-> ")
        intlevel = input("On a scale from 1-10 how interested are you in this?\n-> ")
        skill = input("List a skill that you possess:\n-> ")
        skilevel = input("On a scale from 1-10 how skilled are you at this?\n-> ")
        c.execute("INSERT INTO user VALUES (%s,%s,%s,%s,%s,%s)", (x, first, last, phone, address, degree))
        c.execute("INSERT INTO organization VALUES (%s,%s,%s)", (x, org, orgtype))
        c.execute("INSERT INTO interest VALUES (%s,%s,%s)", (x, interest, intlevel))
        c.execute("INSERT INTO project VALUES (%s,%s)", (x, project))
        c.execute("INSERT INTO skill VALUES (%s,%s,%s)", (x, skill, skilevel))
        x += 1
    elif key == '2':
        cur = conn.cursor()
        first, last = input("Enter the first and last name of the user.\n-> ").split()
        cur.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
        userset = (cur.fetchone())
        print('-> The users first name is: ', userset[1])
        print('-> The users last name is: ', userset[2])
        print('-> The users phone number is: ', userset[3])
        print('-> The users address is: ', userset[4])
        print('-> The user has a degree in: ', userset[5])
    elif key == '0':
        print("Thank you for using our software")
        break
    else:
        print("This input was not recognized.")

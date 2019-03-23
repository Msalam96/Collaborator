import csv
import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", passwd="password", database="collaboratordb")

c = conn.cursor(buffered=True)

c.execute("CREATE DATABASE IF NOT EXISTS collaboratordb")

c.execute("""CREATE TABLE IF NOT EXISTS user (
        user_id text,
        first text,
        last text
        # phone text,
        # address text,
        # degree text 
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS interest (
        user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        interest text,
        interest_level integer
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS distance (
        org1 text,
        org2 text,
        distance real
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS organization (
        user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        org_name text,
        org_type text
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS project (
        user_id text,
        proj_name text
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS skill (
        user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        skill_name text,
        skill_level integer
        )""")


def simInterests(userId):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interest WHERE user_id=%s", (userId,))
    sInterest = (cursor.fetchone())
    print(sInterest)
    cursor.execute("SELECT * FROM interest WHERE interest = %s", (sInterest[0],))
    intInfo = (cursor.fetchall())
    print(intInfo)
    for data in cursor:
        print("\nWe in the for loop at iteration #", x)
        cursor.execute("SELECT * FROM user WHERE user_id = %s", (intInfo[0],))
        print("\nFirst SQL in for loop")
        perInfo = (cursor.fetchone())
        cursor.execute("SELECT org_name FROM organization WHERE user_id = %s", perInfo[0], )
        compInfo = (cursor.fetchone())
        print('%s %s who works at %s has %s in common with you', (perInfo[1], perInfo[2], compInfo, sInterest[0]))


def userexists(f, l):

    c.execute("SELECT * FROM user WHERE first=%s AND last=%s", (f, l))
    row = c.rowcount
    return row == 1


user_data = csv.reader(open('user.csv'))
project_data = csv.reader(open('project.csv'))

firstline = True
firstline2 = True

for row in user_data:
    if firstline:
        firstline = False
        continue
    else:
        c.execute('INSERT INTO user(user_id, \
                first, last )' \
                'VALUES(%s, %s, %s)',
                row)
        print(row)

for row in project_data:
    if firstline2:
        firstline2 = False
        continue
    else:
        c.execute('INSERT INTO project(user_id, \
                proj_name)' \
                'VALUES(%s, %s)',
                row)
        print(row)

print("Welcome to the Collaborator Software. The CSV files have been read! Here are the following inputs:")
while True:
    key = input(""" 
Press 1 to find information about a specific user. 
Press 2 to find collaborators to a user. 
Press 0 to exit \n-> """)
    if key == '1':
        cur = conn.cursor()
        first, last = input("Enter the first and last name of the user.\n-> ").split()
        if userexists(first,last):
            cur.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
            userset = (cur.fetchone())
            print('-> The users id is: ', userset[0])
            print('-> The users first name is: ', userset[1])
            print('-> The users last name is: ', userset[2])
            # print('-> The users phone number is: ', userset[3])
            # print('-> The users address is: ', userset[4])
            # print('-> The user has a degree in: ', userset[5])
        else:
            print("-> Sorry, this user does not exist.")
    elif key == '2':
        cur = conn.cursor()
        first, last = input("Enter the first and last name of the user to collaborate with.\n-> ").split()
        if userexists(first,last):
            query = """SELECT user.user_id, user.first, user.last, project.user_id, project.proj_name
                FROM user, project
                WHERE first=%s AND last=%s AND user.user_id = project.user_id
                ORDER BY user.user_id"""
            cur.execute(query, (first, last))
            rows = cur.fetchall()
            for row in rows:
                idv = row[0]
                proj = row[4]
                ids = []
                query2 = """SELECT * FROM project WHERE proj_name IN(
                    SELECT proj_name FROM project
                    WHERE proj_name=%s
                    GROUP BY proj_name HAVING count(*) > 1 )"""
                cur.execute(query2, (row[4],))
                rows2 = cur.fetchall()
                for row2 in rows2:
                    ids.append(row2[0])
                query3 = "SELECT * FROM user WHERE user_id=%s"
                print("-> Here is a list of trusted colleague(s) for project ", row[4], ":")
                for x in range(len(ids)):
                    cur.execute(query3, (ids[x],))
                    rows3 = cur.fetchall()
                    for row3 in rows3:
                        if idv == row3[0]:
                            pass
                        else:
                            print("-> ", row3[1], row3[2])
        else:
            print("-> Sorry this user does not exist.")
    elif key == '0':
        print("Thank you for using our software")
        break
    else:
        print("This input was not recognized.")


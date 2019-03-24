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
        user_id text,
        interest text,
        interest_level integer
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS distance (
        org1 text,
        org2 text,
        distance real
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS organization (
        user_id text,
        org_name text,
        org_type text
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS project (
        user_id text,
        proj_name text
        )""")

c.execute("""CREATE TABLE IF NOT EXISTS skill (
        user_id text,
        skill_name text,
        skill_level integer
        )""")

def userexists(f, l):
    c.execute("SELECT * FROM user WHERE first=%s AND last=%s", (f, l))
    row = c.rowcount
    return row == 1


def custom_sort(t):
    return t[4]


def sim_interests():
    data_interest = []
    first, last = input("Enter the first and last name of the user.\n-> ").split()
    if userexists(first, last):
        c.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
        user_info = c.fetchone()
        c.execute("SELECT * FROM interest WHERE user_id = %s", (user_info[0],))
        comm_interests = (c.fetchall())
        for s_interest in comm_interests:
            c.execute("SELECT * FROM interest WHERE interest = %s", (s_interest[1],))
            int_info = (c.fetchall())
            for data in int_info:
                if user_info[0] == data[0]:
                    continue
                c.execute("SELECT * FROM user WHERE user_id = %s", (data[0],))
                per_info = (c.fetchone())
                c.execute("SELECT org_name FROM organization WHERE user_id = %s", (per_info[0],))
                comp_info = c.fetchone()
                data_interest.append([per_info[1], per_info[2], comp_info[0], s_interest[1], data[2]])
            print("Here is a list of other users who share an interest in", s_interest[1], ":")
            data_interest.sort(key=custom_sort, reverse=True)
            for data in data_interest:
                print("-> ", data[0], data[1], "who works at", data[2], "with level", data[4])
    else:
        print("-> Sorry, this user does not exist.")


def sim_skills():
    data_interest = []
    first, last = input("Enter the first and last name of the user.\n-> ").split()
    if userexists(first, last):
        c.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
        user_info = c.fetchone()
        c.execute("SELECT * FROM skill WHERE user_id = %s", (user_info[0],))
        commSkills = (c.fetchall())
        for each_skill in commSkills:
            c.execute("SELECT * FROM skill WHERE skill_name = %s", (each_skill[1],))
            int_info = (c.fetchall())
            for data in int_info:
                if user_info[0] == data[0]:
                    continue
                c.execute("SELECT * FROM user WHERE user_id = %s", (data[0],))
                per_info = (c.fetchone())
                c.execute("SELECT org_name FROM organization WHERE user_id = %s", (per_info[0],))
                comp_info = c.fetchone()
                data_interest.append([per_info[1], per_info[2], comp_info[0], each_skill[1], data[2]])
            print("Here is a list of other uers who share a skill in", each_skill[1], ":")
            data_interest.sort(key=custom_sort, reverse=True)
            for data in data_interest:
                print("-> ", data[0], data[1], "who works at", data[2], "with level", data[4])
    else:
        print("-> Sorry, this user does not exist.")


def details():
    cur = conn.cursor()
    try:
        first, last = input("Enter the first and last name of the user.\n-> ").split()
        if userexists(first, last):
            cur.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
            userset = (cur.fetchone())
            uid = userset[0]
            #print('-> The users id is: ', userset[0])
            print('-> The users first name is: ', userset[1])
            print('-> The users last name is: ', userset[2])
            # print('-> The users phone number is: ', userset[3])
            # print('-> The users address is: ', userset[4])
            # print('-> The user has a degree in: ', userset[5])
            query = "SELECT * FROM project WHERE user_id=%s"
            cur.execute(query, (uid,))
            userset2 = cur.fetchall()
            print("-> Projects this user has worked on are: ")
            for row in userset2:
                print("-> ", row[1])
            query2 = "SELECT * FROM interest WHERE user_id=%s"
            cur.execute(query2, (uid,))
            userset3 = cur.fetchall()
            print("-> Interests this user has are: ")
            for row2 in userset3:
                print("-> ", row2[1])
            query3 = "SELECT * FROM skill WHERE user_id=%s"
            cur.execute(query3, (uid,))
            userset4 = cur.fetchall()
            print("-> Skills this user has are: ")
            for row3 in userset4:
                print("-> ", row3[1])
            query4 = "SELECT * FROM organization WHERE user_id=%s"
            cur.execute(query4, (uid,))
            userset5 = cur.fetchone()
            print("-> This user's organization is: ", userset5[1])
        else:
            print("-> Sorry, this user does not exist.")
    except ValueError:
        print("-> This input is invalid.")


def collaborators():
    cur = conn.cursor()
    try:
        first, last = input("Enter the first and last name of the user to collaborate with.\n-> ").split()
        if userexists(first, last):
            query = """SELECT user.user_id, user.first, user.last, project.user_id, project.proj_name
                        FROM user, project
                        WHERE first=%s AND last=%s AND user.user_id = project.user_id
                        ORDER BY user.user_id"""
            cur.execute(query, (first, last))
            rows = cur.fetchall()
            for row in rows:
                idv = row[0]
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
                print("-> Here is a list of trusted colleague(s) for project:", row[4], ":")
                for x in range(len(ids)):
                    cur.execute(query3, (ids[x],))
                    rows3 = cur.fetchall()
                    count = cur.rowcount
                    for row3 in rows3:
                        if idv == row3[0]:
                            pass
                        elif count == 0:
                            print("-> No Collaborators")
                        else:
                            print("-> ", row3[1], row3[2])
        else:
            print("-> Sorry this user does not exist.")
    except ValueError:
        print("This input is valid.")


user_data = csv.reader(open('user.csv'))
project_data = csv.reader(open('project.csv'))
interest_data = csv.reader(open('interest.csv'))
org_data = csv.reader(open('organization.csv'))
skill_data = csv.reader(open('skill.csv'))
dist_data = csv.reader(open('distance.csv'))

firstline = True
firstline2 = True
firstline3 = True
firstline4 = True
firstline5 = True
firstline6 = True

for row in user_data:
    if firstline:
        firstline = False
        continue
    else:
        c.execute('INSERT INTO user(user_id,first, last ) VALUES(%s, %s, %s)', row)

for row in project_data:
    if firstline2:
        firstline2 = False
        continue
    else:
        c.execute('INSERT INTO project(user_id, proj_name) VALUES(%s, %s)', row)

for row in interest_data:
    if firstline3:
        firstline3 = False
        continue
    else:
        c.execute('INSERT INTO interest(user_id, interest, interest_level) VALUES(%s, %s, %s)', row)

for row in org_data:
    if firstline4:
        firstline4 = False
        continue
    else:
        c.execute('INSERT INTO organization(user_id, org_name, org_type) VALUES(%s, %s, %s)', row)

for row in skill_data:
    if firstline5:
        firstline5 = False
        continue
    else:
        c.execute('INSERT INTO skill(user_id, skill_name, skill_level) VALUES(%s, %s, %s)', row)

for row in dist_data:
    if firstline6:
        firstline6 = False
        continue
    else:
        c.execute('INSERT INTO distance(org1, org2, distance) VALUES(%s, %s, %s)', row)

print("Welcome to the Collaborator Software. The CSV files have been read! Here are the following inputs:")
while True:
    key = int(input(""" 
Press 1 to find information about a specific user. 
Press 2 to find collaborators to a user. 
Press 3 to find a user with similar interests.
Press 4 to find a user with a common skill.
Press 5 to find a trusted colleague. 
Press 0 to exit \n-> """))
    if key == 1:
        details()
    elif key == 2:
        collaborators()
    elif key == 3:
        sim_interests()
    elif key == 4:
        sim_skills()
    elif key == 0:
        print("Thank you for using our software")
        break
    else:
        print("This input was not recognized.")


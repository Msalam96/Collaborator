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


def sim_skills():
    data_interest = []
    first, last = input("Enter the first and last name of the user.\n-> ").split()
    if userexists(first, last):
        c.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
        user_info = c.fetchone()
        c.execute("SELECT org_name FROM organization WHERE user_id = %s", (user_info[0],))
        first_location = c.fetchone()
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
                c.execute("SELECT org_name,org_type FROM organization WHERE user_id = %s", (per_info[0],))
                comp_info = c.fetchone()
                c.execute("SELECT distance FROM distance WHERE org1=%s AND org2=%s", (first_location[0], comp_info[0]))
                dist_info = c.fetchone()
                print(dist_info[0])
                data_interest.append([per_info[1], per_info[2], comp_info[0], each_skill[1], data[2], comp_info[1], dist_info[0]])
                if not data_interest:
                    continue
                else:
                    if dist_info[0] > 10:
                        continue
                    else:
                        print("Here is a list of other users who share a skill in", each_skill[1], ":")
                        data_interest.sort(key=custom_sort, reverse=True)
                        for data in data_interest:
                            print("-> ", data[0], data[1], "who works at", data[2], "with level", data[4])
    else:
        print("-> Sorry, this user does not exist.")


    # result = {}
    # print("\nInfo in mdata_interest: ")
    # for info in mdata_interest:
    #     if info[1]
    #
    # for i in range (1,len(mdata_interest)):
    #     for info in mdata_interest:
    #         if info[0] == info[i]:
    #             print("this works")
    # for info in mdata_interest:
    #     key = info[0] + info[1]
    #     total = result.get(key,0) + info[4]
    #     result[info[0], info[1], info[2], info[3]] = total
    #
    # print("Here is the result dict: ", result)
    #
    # interests = collections.defaultdict(int)
    # for data in mdata_interest:
    #     first, last, org, interest, level = data
    #     interests[(first,last,org,interest)] += level
    # print("\ndict(result) = ", dict(interests))


def sim_interests():
    mdata_interest = []
    first, last = input("Enter the first and last name of the user.\n-> ").split()
    if userexists(first, last):
        c.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
        user_info = c.fetchone()
        c.execute("SELECT org_name FROM organization WHERE user_id = %s", (user_info[0],))
        first_location = c.fetchone()
        c.execute("SELECT * FROM interest WHERE user_id = %s", (user_info[0],))
        comm_interests = (c.fetchall())
        for s_interest in comm_interests:
            data_interest = []
            c.execute("SELECT * FROM interest WHERE interest = %s", (s_interest[1],))
            int_info = (c.fetchall())
            for data in int_info:
                if user_info[0] == data[0]:
                    continue
                c.execute("SELECT * FROM user WHERE user_id = %s", (data[0],))
                per_info = (c.fetchone())
                c.execute("SELECT org_name FROM organization WHERE user_id = %s", (per_info[0],))
                comp_info = c.fetchone()
                c.execute("SELECT distance FROM distance WHERE org1=%s AND org2=%s", (first_location[0], comp_info[0]))
                dist_info = c.fetchone()
                #print("DISTANCE INFO: ", dist_info[0])
                data_interest.append([per_info[1], per_info[2], comp_info[0], s_interest[1], data[2], dist_info[0]])
            if not data_interest:
                continue
            else:
                print("Here is a list of other users who share an interest in", s_interest[1], ":")
                data_interest.sort(key=custom_sort, reverse=True)
                for data in data_interest:
                    if data[5] > 10:
                        pass
                    else:
                        print("-> ", data[0], data[1], "who works at", data[2], "has a skill level of", data[4], "and works", data[5], "miles from you.")
                        mdata_interest.append(data)
    else:
        print("-> Sorry, this user does not exist.")


# def trusted_coll():
#     first, last = input("Enter the first and last name for whom you would like to find trusted colleagues. \n ").split()
#     if userexists(first, last):
#         c.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
#         user_info = c.fetchone()
#         c.execute("SELECT org_name FROM organization WHERE user_id=%s", (user_info[0],))
#         user_org = c.fetchone()
#         c.execute("SELECT user_id FROM organization WHERE org_name=%s", (user_org[0],))
#         coworkers = c.fetchall()
#         for each coworker in coworkers:
#             c.execute("SELECT ")
#
#     else:
#         print("-> Sorry, this user does not exist.")


def details():
    cur = conn.cursor()
    try:
        first, last = input("Enter the first and last name of the user.\n-> ").split()
        if userexists(first, last):
            cur.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
            userset = (cur.fetchone())
            uid = userset[0]
            #print('-> The users id is: ', userset[0])
            print('-> The users first name is:', userset[1])
            print('-> The users last name is:', userset[2])
            # print('-> The users phone number is: ', userset[3])
            # print('-> The users address is: ', userset[4])
            # print('-> The user has a degree in: ', userset[5])
            query = "SELECT * FROM project WHERE user_id=%s"
            cur.execute(query, (uid,))
            userset2 = cur.fetchall()
            print("-> Projects this user has worked on are:")
            for row in userset2:
                print("-> ", row[1])
            query2 = "SELECT * FROM interest WHERE user_id=%s"
            cur.execute(query2, (uid,))
            userset3 = cur.fetchall()
            print("-> Interests this user has are:")
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
            print("-> This user's organization is:", userset5[1])
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
                            print("->", row3[1], row3[2])
        else:
            print("-> Sorry this user does not exist.")
    except ValueError:
        print("This input is invalid.")


def distances():
    cur = conn.cursor()
    try:
        first, last = input("Enter the first and last name of the user to find nearby organizations.\n-> ").split()
        if userexists(first, last):
            cur.execute("SELECT * FROM user WHERE first=%s AND last=%s", (first, last))
            userset = (cur.fetchone())
            uid = userset[0]
            query = "SELECT * FROM organization WHERE user_id=%s"
            cur.execute(query,(uid,))
            rows = cur.fetchone()
            org = rows[1]
            query2 = "SELECT * FROM distance WHERE org1=%s AND distance < 10"
            cur.execute(query2,(org,))
            rows2 = cur.fetchall()
            for row in rows2:
                print("->", row[1], "is", row[2], "miles from", row[0], ".")
    except ValueError:
        print("This input is valid.")


file1 = input("-> Enter the user csv file to be read: ")
user_data = csv.reader(open(file1))
firstline = True
for row in user_data:
    if firstline:
        firstline = False
        continue
    else:
        c.execute('INSERT IGNORE INTO user(user_id,first, last ) VALUES(%s, %s, %s)', row)

file2 = input("-> Enter the project csv file to be read: ")
project_data = csv.reader(open(file2))
firstline2 = True
for row in project_data:
    if firstline2:
        firstline2 = False
        continue
    else:
        c.execute('INSERT IGNORE INTO project(user_id, proj_name) VALUES(%s, %s)', row)

file3 = input("-> Enter the interest csv file to be read: ")
interest_data = csv.reader(open(file3))
firstline3 = True
for row in interest_data:
    if firstline3:
        firstline3 = False
        continue
    else:
        c.execute('INSERT IGNORE INTO interest(user_id, interest, interest_level) VALUES(%s, %s, %s)', row)

file4 = input("-> Enter the organization csv file to be read: ")
org_data = csv.reader(open(file4))
firstline4 = True
for row in org_data:
    if firstline4:
        firstline4 = False
        continue
    else:
        c.execute('INSERT IGNORE INTO organization(user_id, org_name, org_type) VALUES(%s, %s, %s)', row)

file5 = input("-> Enter the skill csv file to be read: ")
skill_data = csv.reader(open(file5))
firstline5 = True
for row in skill_data:
    if firstline5:
        firstline5 = False
        continue
    else:
        c.execute('INSERT IGNORE INTO skill(user_id, skill_name, skill_level) VALUES(%s, %s, %s)', row)

file6 = input("-> Enter the distance csv file to be read: ")
dist_data = csv.reader(open(file6))
firstline6 = True
for row in dist_data:
    if firstline6:
        firstline6 = False
        continue
    else:
        c.execute('INSERT IGNORE INTO distance(org1, org2, distance) VALUES(%s, %s, %s)', row)

print("Welcome to the Collaborator Software. The CSV files have been read! Here are the following inputs:")
while True:
    key = input(""" 
Press 1 to find information about a specific user. 
Press 2 to find collaborators to a user. 
Press 3 to find a user with similar interests.
Press 4 to find a user with a common skill.
Press 5 to find organizations within 10 miles from a user.
Press 0 to exit \n-> """)
    if key == '1':
        details()
    elif key == '2':
        collaborators()
    elif key == '3':
        sim_interests()
    elif key == '4':
        sim_skills()
    elif key == '5':
        distances()
    elif key == '0':
        print("Thank you for using our software")
        break
    else:
        print("This input was not recognized.")
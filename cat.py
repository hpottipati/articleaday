import psycopg2
def getRowsFromDatabase(postgreSQL_select_Query):
    try:
        connection = psycopg2.connect(user="postgres",
                            password="NWC_if3eTGyHWGRon1UcrEy7iRsPGm5p",
                            host="localhost",
                            port="5432",
                            database="postgres")
        cursor = connection.cursor()

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from mobile table using cursor.fetchall")
        user_id = cursor.fetchall()
        return user_id

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

#!/usr/bin/python

def sql_request(sql):
    vendor_id = None
    conn = None
    
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(user="postgres",
                                    password="NWC_if3eTGyHWGRon1UcrEy7iRsPGm5p",
                                    host="localhost",
                                    port="5432",
                                    database="postgres")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the generated id back
        #vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR')
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return vendor_id

def getUserID():
    returnstatement = getRowsFromDatabase("SELECT user_id FROM account_emailaddress WHERE email='hackphoenix2021@gmail.com';")[0]
    return returnstatement[0]

user_id = getUserID()
sql_request(f"INSERT INTO user_folderid(user_id,folder_id) VALUES ({user_id}, 'cat');")
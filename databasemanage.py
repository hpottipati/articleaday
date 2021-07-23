import psycopg2

sql='ALTER ROLE ujfijzsb CONNECTION LIMIT -1;'


conn = psycopg2.connect(user="ujfijzsb",
                                    password="NWC_if3eTGyHWGRon1UcrEy7iRsPGm5p",
                                    host="batyr.db.elephantsql.com",
                                    port="5432",
                                    database="ujfijzsb")
# create a new cursor
cur = conn.cursor()
# execute the INSERT statement
cur.execute(sql)

print('completed finishing in your mom')
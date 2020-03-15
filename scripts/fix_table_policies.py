import psycopg2
import json

connection = psycopg2.connect(host="localhost", database="twitter_postgres", user="admin", password="admin")

cursor = connection.cursor()
cursor.execute("select * from api;")
api_data = dict(cursor.fetchall())
connection.commit()
cursor.close()


cursor = connection.cursor()
cursor.execute("select * from filter;")
filter_data = dict(cursor.fetchall())
connection.commit()
cursor.close()  



cursor = connection.cursor()
cursor.execute("select id_policy,api_type,filter from policies;")
policies_data = cursor.fetchall()
connection.commit()
cursor.close()


# Alter data type
cursor = connection.cursor()
cursor.execute("alter table policies alter column api_type TYPE TEXT;")
cursor.execute("alter table policies alter column filter TYPE TEXT;")
connection.commit()
cursor.close()



for data in policies_data:
    id,api_type,filter = data
    api_value,filter_value = api_data[int(api_type)],filter_data[int(filter)]
    
    cursor = connection.cursor()
    cursor.execute(f"update policies set api_type = '{api_value}', filter = '{filter_value}' where id_policy={int(id)} ")
    connection.commit()
    cursor.close()


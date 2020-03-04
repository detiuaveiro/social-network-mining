import psycopg2
import json
BOTS_IDS = ["1129479987206205440","1103294806497902594","1131301906679324672","1129390603031207937","1129475305444388866","1132271132462256129"]


connection = psycopg2.connect(host="localhost", database="twitter_postgres", user="admin", password="admins")

# Add field
try:
    cursor = connection.cursor()
    cursor.execute("alter table policies add column bots bigint[];")
    connection.commit()
    cursor.close()
except Exception as e:
    connection.commit()
    cursor.close()


#Get data
cursor = connection.cursor()
cursor.execute("select id_policy,params from policies;")
data = cursor.fetchall()
connection.commit()
cursor.close()



#Update fields
for entry in data:
    id,params = entry[0:2]
    new_params = []
    bots = []
    for p in params:
        if p not in BOTS_IDS:
            new_params.append(p)
        else:
            bots.append(int(p))
    if len(bots) == 0:
        continue
    cursor = connection.cursor()
    sql_params = json.dumps(new_params,ensure_ascii=False).replace('[','{').replace(']','}')
    sql_bots = set(bots)
    
    cursor.execute(f"update policies set params = '{sql_params}', bots = '{sql_bots}' where id_policy={int(id)} ")
    connection.commit()
    cursor.close()

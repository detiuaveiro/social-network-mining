import sqlite3
import json
from calendar import monthrange
from ast import literal_eval
from datetime import datetime

sql_transaction = []

connection = sqlite3.connect('database.db')
c = connection.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS parent_reply(parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, comment TEXT, subreddit TEXT, unix INT, score INT)")

def format_data(data):
    data = data.replace('\n',' newlinechar ').replace('\r',' newlinechar ').replace('"',"'")
    return data

def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as e:
        #print(str(e))
        return False

def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as e:
        #print(str(e))
        return False

def acceptable(data):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]':
        return False
    elif data == '[removed]':
        return False
    else:
        return True

def sql_insert_replace_comment(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))

def sql_insert_has_parent(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))


def sql_insert_no_parent(commentid,parentid,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))

def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []

if __name__ == '__main__':
    create_table()
    years=['2018','2017','2016','2015','2014','2013','2012','2011']
    months=['01','02','03','04','05','06','07','08','09','10','11','12']

    def dateformater(years,months):
        row_counter = 0
        paired_rows = 0
        for year in years:
            for month in months:
                (first,last) = monthrange(int(year),int(month))
                days = ranges(last,10)
                for day in days:
                    (f,l) = literal_eval(day)
                    after=year+"-"+month+"-"+"{0:0=2d}".format(f)
                    before=year+"-"+month+"-"+"{0:0=2d}".format(l)
                    with open('./data/data({}_{}).json'.format(after,before), buffering=1000) as f:
                        t = json.loads(f.read())
                        for row in t['data']:
                            row_counter += 1
                            parent_id = row['parent_id']
                            body = format_data(row['body'])
                            created_utc = row['created_utc']
                            score = row['score']
                            comment_id = row['id']
                            subreddit = row['subreddit']
                            parent_data = find_parent(parent_id)
                            # maybe check for a child, if child, is our new score superior? If so, replace. If not...

                            if score >= 2:
                                existing_comment_score = find_existing_score(parent_id)
                                if existing_comment_score:
                                    if score > existing_comment_score:
                                        if acceptable(body):
                                            sql_insert_replace_comment(comment_id,parent_id,parent_data,body,subreddit,created_utc,score)
                                else:
                                        if acceptable(body):
                                            if parent_data:
                                                sql_insert_has_parent(comment_id,parent_id,parent_data,body,subreddit,created_utc,score)
                                                paired_rows += 1
                                            else:
                                                sql_insert_no_parent(comment_id,parent_id,body,subreddit,created_utc,score)
                            
                            if row_counter % 100000 == 0:
                                print('Total Rows Read: {}, Paired Rows: {}, Time: {}'.format(row_counter, paired_rows, str(datetime.now())))


    def ranges(N, nb):
        step = N / nb
        return ["({},{})".format(round(step*i)+1, round(step*(i+1))) for i in range(nb)]

    dateformater(years,months)

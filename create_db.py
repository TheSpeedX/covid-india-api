import sqlite3
from sqlite3 import Error
import string
database = r"firebase.db"

def create_table(conn, create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)
def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	return conn

def create_state(conn, state):
	if check_state(conn,state):
		return False
	cur = conn.cursor()
	sql = ''' INSERT INTO information(state) VALUES(?) '''
	cur.execute(sql, (state,))
	conn.commit()
	return cur.rowcount >=1
def check_state(conn,state):
	cur = conn.cursor()
	cur.execute("SELECT state FROM information WHERE state = ?", (state,))
	data=cur.fetchall()
	return len(data)>0
def clear_latest(conn):
	cur = conn.cursor()
	cur.execute('''DELETE FROM latest;''')
	conn.commit()
	cur = conn.cursor()
	cur.execute('''DELETE FROM report;''')
	conn.commit()
def update_state(conn,state,cases,cured,death):
	cur = conn.cursor()
	state=state.lower()
	if not check_state(conn,state):
		sql = ''' INSERT INTO information(state) VALUES(?) '''
		cur.execute(sql, (state,))
	sdata=fetch_state(state)
	pcases=int(cases)-int(sdata['cases'])
	pcured=int(cured)-int(sdata['cured'])
	pdeath=int(death)-int(sdata['death'])
	if pcases<=0 and pcured==0 and pdeath==0:
		conn.commit()
		return False
	sql = ''' INSERT INTO latest(state,cases,cured,death) VALUES(?,?,?,?) '''
	cur.execute(sql, (state,pcases,pcured,pdeath))
	sql = '''UPDATE information SET cases = ? , cured = ? , death = ? WHERE state =? '''
	cur.execute(sql, (cases,cured,death,state))
	conn.commit()
def update_news(news):
	conn=create_connection(database)
	cur = conn.cursor()
	sql = '''UPDATE report SET news = ? '''
	cur.execute(sql, (news,))
	conn.commit()
	return cur.rowcount >=1
def gen_new_report():
	conn=create_connection(database)
	conn=create_connection(database)
	cur = conn.cursor()
	cur.execute('''SELECT state,cases,cured,death FROM latest; ''')
	data=cur.fetchall()
	full=[]
	suffix=[" new positive cases has been reported in "," people successfully cured of corona in "," people reported death by corona in "]
	for row in data:
		semi=[]
		for cell in range(1,4):
			if row[cell]!=0:
				semi.append(str(row[cell])+suffix[cell-1]+string.capwords(str(row[0])))
		full.append("\n".join(semi))
	fullreport="\n".join(full)
	cur.execute('''SELECT sum(cases),sum(cured),sum(death) FROM information; ''')
	data=cur.fetchall()[0]
	sql = ''' INSERT INTO report(casereport,cases,cured,death) VALUES(?,?,?,?) '''
	cur.execute(sql, (fullreport,data[0],data[1],data[2]))
	conn.commit()
	return cur.rowcount >=1
def fetch_state(state):
	conn=create_connection(database)
	state=state.lower()
	sql = '''SELECT cases,cured,death FROM information WHERE state = ? '''
	cur = conn.cursor()
	cur.execute(sql, (state,))
	try:
		data=cur.fetchall()[0]
		return {"cases":data[0],"cured":data[1],"death":data[2]}
	except:
		return {"cases":0,"cured":0,"death":0}
def fetch_all():
	conn=create_connection(database)
	cur = conn.cursor()
	cur.execute('''SELECT state,cases,cured,death FROM information ;''')
	data=cur.fetchall()
	full=[]
	try:
		for row in data:
			full.append({"state":row[0],"cases":row[1],"cured":row[2],"death":row[3]})
		return {"all":full}
	except:
		return {"status":"failed"}
def fetch_news():
	conn=create_connection(database)
	cur = conn.cursor()
	cur.execute('''SELECT news FROM report; ''')
	data=cur.fetchall()
	try:
		return data[0][0]
	except:
		return ""
def fetch_report():
	conn=create_connection(database)
	cur = conn.cursor()
	cur.execute('''SELECT casereport FROM report; ''')
	data=cur.fetchall()
	try:
		return data[0][0]
	except:
		return ""
def fetch_total():
	conn=create_connection(database)
	cur = conn.cursor()
	cur.execute('''SELECT cases,cured,death FROM report; ''')
	data=cur.fetchall()[0]
	try:
		return {"cases":data[0],"cured":data[1],"death":data[2]}
	except:
		return {"cases":0,"cured":0,"death":0}
def predict(state):
	conn=create_connection(database)
	lcases=fetch_state(state)['cases']
	tcases=fetch_total()['cases']
	cur = conn.cursor()
	cur.execute('''SELECT max(cases) FROM information; ''')
	data=int(cur.fetchall()[0][0])
	tcases=(data+tcases)/2.0	
	probability=(lcases*100.0)/tcases
	return {"probability":probability}
def main():
	sql_create_info_table = """ CREATE TABLE IF NOT EXISTS information (
										id integer PRIMARY KEY,
										state text NOT NULL,
										cases number DEFAULT 0,
										cured number DEFAULT 0,
										death number DEFAULT 0
									); """
	sql_create_update_table = """ CREATE TABLE IF NOT EXISTS latest (
										id integer PRIMARY KEY,
										state text NOT NULL,
										cases number DEFAULT 0,
										cured number DEFAULT 0,
										death number DEFAULT 0
									); """
	sql_create_report_table = """ CREATE TABLE IF NOT EXISTS report (
										id integer PRIMARY KEY,
										news text DEFAULT "",
										casereport text DEFAULT "",
										cases number DEFAULT 0,
										cured number DEFAULT 0,
										death number DEFAULT 0
									); """
	# create a database connection
	conn = create_connection(database)
 
	# create tables
	if conn is not None:
		# create projects table
		create_table(conn, sql_create_info_table)
		create_table(conn, sql_create_update_table)
		create_table(conn, sql_create_report_table)
 
	else:
		print("Error! cannot create the database connection.")

main()
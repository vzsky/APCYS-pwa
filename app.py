from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flaskext.mysql import MySQL
import jwt
import requests
import json

app = Flask(__name__)
mysql = MySQL()

# Settings ###########################################################################################################

app.config['SECRET_KEY'] = 'secret'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'APCYS'
app.config['MYSQL_DATABASE_HOST'] = '10.205.240.11'

port = 7000

mysql.init_app(app)

api_url = 'http://0.0.0.0:'+port+'/api/login'
api_tok = 'http://0.0.0.0:'+port+'/api/token'
api_add = 'http://0.0.0.0:'+port+'/api/addanc'

# END SETTINGS #######################################################################################################

# API HERE ###########################################################################################################

def auth(usr,pwd):
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM User WHERE Usr='" + usr + "' and Pwd='" + pwd + "'")
	data = cursor.fetchone()
	cursor.close()
	connection.close()
	if data is None:
		return jsonify({"status" : "denied"})
	token = jwt.encode({"user":usr}, app.config['SECRET_KEY'])
	return jsonify({"status" : "accepted" , "token" : token.decode("utf-8") })

def update(id, table, col, val):
	connection = mysql.connect()
	cursor = connection.cursor()
	print("Run : UPDATE " + table + " SET " + col + " = " + val + " WHERE id = "+id+";")
	cursor.execute("UPDATE " + table + " SET " + col + " = " + val + " WHERE id = "+id+";")
	connection.commit()
	cursor.close()
	connection.close()

@app.route('/api/login', methods=['POST'])
def apilogin():
	#AUTHEN TOKEN - NO TIMEOUT
	try :
		data = request.json
		usr = data["user"]
		pwd = data["pass"]
		token = auth(usr,pwd)
	except : 
		token = auth(usr,pwd)
	return token

@app.route('/api/token', methods=['POST'])
def tkauth():
	try:
		#GATHER ALL DATA + CHECK TOKEN
		token = request.headers['token']
		send = jwt.decode(token, app.config['SECRET_KEY'])
		user = send["user"]
		connection = mysql.connect()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM User WHERE Usr='" + user + "'")
		data = cursor.fetchone()
		send["id"] = data[0] 
		send["name"] = data[3]
		send["res"] = data[4]
		send["present"] = data[5]
		send["country"] = data[6]
		send["school"] = data[7]
		send["sciact"] = data[8]
		send["project"] = data[9]
		buddies=[]
		for x in range(10,14):
			if data[x] is not None :
				buddies.append(data[x]);
		send["buddies"] = buddies
		send["logged"] = data[14]
		cursor.execute("SELECT * FROM announce")
		anc = cursor.fetchall()
		cursor.close()
		connection.close()
	except:
		return jsonify({"error":"authen error"})
	return jsonify({"user":send,"announce":anc})

@app.route('/api/addanc', methods=['POST'])
def addanc():
	try :
		data = request.json
		top = data["topic"]
		con = data["content"]
		connection = mysql.connect()
		cursor = connection.cursor()
		cursor.execute("SELECT MAX(id) from announce")
		maxid = cursor.fetchone()
		try : 
			postid = maxid[0] + 1
		except : 
			postid = 0
		cursor.execute("INSERT INTO announce (id,topic,content) VALUES (%s,%s,%s)",(postid, top, con))
		connection.commit()
		status = "POSTed"
		cursor.close()
		connection.close()
	except :
		status = "error"
	return status

#API END HERE #######################################################################################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
	if 'token' in session:
		headers = {'token': session['token']}
		r = requests.post(url=api_tok, headers=headers)
		datare = r.json()
		if 'error' in datare :
			return render_template("login.html")
		userinfo = datare['user']
		if userinfo['user'] == 'admin' :
			return redirect(url_for('admin'))
		return redirect(url_for('index'))

	if request.method == 'POST':
		usr = request.form['usr']
		pwd = request.form['pwd']
		row_data = {"user": usr,"pass":pwd}
		print(row_data)
		r = requests.post(url=api_url, json=row_data)
		datare = r.json()
		token = datare['token']
		print(token)
		session['token'] = token
		return redirect(url_for('login'))
	return render_template("login.html")

@app.route('/', methods=['GET', 'POST'])
def index ():
	try :
		page = request.args.get('page')
		page = page + '.html'
	except :
		page = 'index.html'
	if 'token' in session:
		headers = {'token': session['token']}
		r = requests.post(url=api_tok, headers=headers)
		datare = r.json()
		if 'error' in datare :
			return redirect(url_for('admin'))
		userinfo = datare['user']
		if userinfo['user'] == 'admin' :
			return redirect(url_for('admin'))
		if userinfo['logged'] == 0:
			return terms(request.method, userinfo['id'])
		return render_template(page, ancs=datare['announce'], name=userinfo['name'], id=userinfo['id'], res=userinfo['res'], present=userinfo['present'], country=userinfo['country'], school=userinfo['school'], sciact=userinfo['sciact'], project=userinfo['project'], buddies=userinfo['buddies'])
	return redirect(url_for('login'))

def terms(method, id):
	if method == 'POST':
		update(str(id), "User", "Logged", "1")
		return redirect(url_for('index'))
	return render_template('terms.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if 'token' in session : 
		headers = {'token': session['token']}
		r = requests.post(url=api_tok, headers=headers)
		datare = r.json()
		if 'error' in datare :
			return redirect(url_for('login'))
		userinfo = datare['user']
		if userinfo['user'] == 'admin' :
			if request.method == 'POST':
				print('post')
				try :
					print('trying')
					topic = request.form['topic']
					content = request.form['content']
					row_data = {"topic": topic, "content":content}
					r = requests.post(url=api_add, json=row_data)
				except : 
					pass
				return redirect(url_for('admin'))
			return render_template('admin.html', ancs=datare['announce'], name=userinfo['name'], id=userinfo['id'], res=userinfo['res'], present=userinfo['present'], country=userinfo['country'], school=userinfo['school'], sciact=userinfo['sciact'], project=userinfo['project'], buddies=userinfo['buddies'])
	return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session.pop('token', None)
	return redirect(url_for('login'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port ,debug = True)
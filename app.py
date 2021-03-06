from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flaskext.mysql import MySQL
import jwt
import requests
import json

app = Flask(__name__)
mysql = MySQL()

# Settings ###########################################################################################################

app.config['SECRET_KEY'] = 'T4Is^f*H3VU$SdGRjgRWu$GiH#*G'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'apcysdb'
app.config['MYSQL_DATABASE_DB'] = 'APCYS'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

port = 80

mysql.init_app(app)

api_url = 'http://localhost/api/login'
api_tok = 'http://localhost/api/token'
api_add = 'http://localhost/api/addanc'

# END SETTINGS #######################################################################################################


@app.before_request
def make_session_permanent():
    session.permanent = True
# API HERE ###########################################################################################################

def auth(usr,pwd):
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM User WHERE username = %s and password = %s;", (usr, pwd))
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
	cursor.execute(""" UPDATE """+ table +""" SET """ + col + """=%s WHERE id=%s """, (val, id))
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
		cursor.execute("SELECT * FROM user WHERE username = %s;", user)
		data = cursor.fetchone()
		print("tokenver")
		#################################################################################
		# Assign key value for each mysql column
		send["id"] = data[0] 
		send['user'] = data[1]
		send["firstn"] = data[3]
		send['lastn'] = data[4]
		send["country"] = data[5]
		send["qrcode"] = data[6]
		send["school"] = data[7]
		send["gender"] = data[8]
		send["position"] = data[9]
		send["residence"] = data[10]
		send["project"] = data[11]
		send["time"] = data[12]
		send["room"] = data[13]
		send["sciact"] = data[14]
		send["xcurs"] = data[15]
		send["buddy"] = data[16]
		send["logged"] = data[17]
		send["projectname"] = data[18]
		send["status"] = data[19]
		#################################################################################
		cursor.execute("SELECT * FROM announce")
		anc = cursor.fetchall()
		cursor.close()
		connection.close()
	except:
		return jsonify({"error":"authen error"})
	return jsonify({"user":send,"announce":anc})

@app.route('/api/addanc', methods=['POST'])
def addanc():
	status = 'started'
	try :
		data = request.json
		headers = {'token':data['token']}
		r = requests.post(url=api_tok, headers=headers)
		datare = r.json()
		if 'error' in datare :
			return redirect(url_for('login'))
		userinfo = datare['user']
		print('userinfo assigned')
		if userinfo['user'] == 'admin' :
			print('should be done!')
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
	print(status)
	return status

#API END HERE #######################################################################################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
	if 'token' in session:
		headers = {'token': session['token']}
		r = requests.post(url=api_tok, headers=headers)
		datare = r.json()
		print(datare)
		if 'error' in datare :
			return render_template("login.html",status="Denied : token verification error")
		userinfo = datare['user']
		if userinfo['user'] == 'admin' :
			return redirect(url_for('admin'))
		return redirect(url_for('index'))

	if request.method == 'POST':
		usr = request.form['usr']
		pwd = request.form['pwd']
		row_data = {"user": usr,"pass":pwd}
		r = requests.post(url=api_url, json=row_data)
		try :
			datare = r.json()
		except :
			return "<h1> Mysql is closed </h1>"
		if datare['status'] == 'accepted':
			token = datare['token']
			session['token'] = token
			return redirect(url_for('login'))
		return render_template("login.html", status="Denied : wrong username or password")
	return render_template("login.html")

@app.route('/main', methods=['GET', 'POST'])
def index ():
	try :
		page = request.args.get('page')
		page = page + '.html'
	except :
		page = 'index.html'
	if 'token' in session:
		headers = {'token': session['token']}
		r = requests.post(url=api_tok, headers=headers)
		print(r)
		try :
			datare = r.json()
		except :
			return "<h1> Mysql is closed </h1>"
		if 'error' in datare :
			return redirect(url_for('admin'))
		userinfo = datare['user']
		if userinfo['user'] == 'admin' :
			return redirect(url_for('admin'))
		print(userinfo['logged'])
		print(userinfo['id'], userinfo['user'])
		if userinfo['logged'] == "0":
			return terms(request.method, userinfo['id'], userinfo['user'], userinfo['firstn'], userinfo['lastn'])
		return render_template(page, data=datare['user'], ancs = datare['announce'][::-1])
	return redirect(url_for('login'))

def terms(method, id, usr, f, l):
	if usr=='terms':
		return render_template('terms.html', first=f, last=l)
	if method == 'POST':
		update(id, 'user', 'logged', '1')
		fi = request.form['first']
		li = request.form['last']
		update(id, 'user', 'first', fi)
		update(id, 'user', 'last', li)
		return redirect(url_for('index'))
	return render_template('terms.html', first=f, last=l)

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
					row_data = {"topic": topic, "content":content, "token":session['token']}
					r = requests.post(url=api_add, json=row_data)
				except : 
					pass
				return redirect(url_for('admin'))
			return render_template('admin.html', data=datare['user'], ancs = datare['announce'])
	return redirect(url_for('login'))

@app.route('/delanc/<id>')
def delanc(id):
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute("DELETE FROM `announce` WHERE id=%s",id)
	connection.commit()
	cursor.close()
	connection.close()
	return redirect(url_for('admin'))

@app.route('/logout')
def logout():
	session.pop('token', None)
	return redirect(url_for('login'))

@app.route('/announcement/<id>')
def announcement(id):
	if 'token' in session : 
		headers = {'token': session['token']}
		r = requests.post(url=api_tok, headers=headers)
		try :
			datare = r.json()
		except :
			return "<h1> Mysql is closed </h1>"
		if 'error' in datare :
			return redirect(url_for('login'))
		ancs = datare['announce']
		for anc in ancs :
			try :
				if int(anc[0])==int(id) :
					return render_template('sanc.html', anc=anc)
			except :
				return render_template('404.html'), 404
		return render_template('noanc.html')
	return redirect(url_for('login'))

@app.route('/check')
def check () :
	cl = []
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM `user` WHERE 1")
	rows = cursor.fetchall()
	for row in rows :
		if (row[19] == 2) :
			b = 'bg-danger'
			cl.append(b)
		else :
			b = 'bg-success'
			cl.append(b)
	x = [c for c, r in enumerate(rows)]
	cursor.close()
	connection.close()
	return render_template('check.html', rows=rows, cl=cl, x=x)

@app.errorhandler(404)
def E404(e):
    return render_template('404.html'), 404

@app.route('/')
def boot():
	return render_template('boot.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port ,debug = True)
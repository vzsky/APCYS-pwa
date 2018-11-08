from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import jwt

app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY'] = 'secret'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'APCYS'
app.config['MYSQL_DATABASE_HOST'] = '10.205.240.221'

#### APP MYSQL CONFIG


mysql.init_app(app)

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

@app.route('/api/login', methods=['POST'])
def login():
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

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7000, debug=True)
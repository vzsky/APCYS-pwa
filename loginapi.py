from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import jwt

app = Flask(__name__)
mysql = MySQL()

from config import *

#### APP MYSQL CONFIG


mysql.init_app(app)

def auth(usr,pwd):
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM User WHERE username='" + usr + "' and password='" + pwd + "'")
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
		cursor.execute("SELECT * FROM User WHERE username='" + user + "'")
		data = cursor.fetchone()
		send["first"] = data[2] #gather Firstname
		send["last"] = data[3]	#gather Lastname
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
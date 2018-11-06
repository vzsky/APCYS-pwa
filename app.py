from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

api_url = 'http://0.0.0.0:7000/api/login'
api_tok = 'http://0.0.0.0:7000/api/token'
api_add = 'http://0.0.0.0:7000/api/addanc'

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

@app.route('/')
def index ():
	try :
		page = request.args.get('page')
		page = page + '.html'
		print(page)
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
		return render_template(page, ancs=datare['announce'], first=userinfo['first'], last=userinfo['last'], user=userinfo['user'])
	return redirect(url_for('login'))

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
			return render_template("admin.html", ancs=datare['announce'], first=userinfo['first'], last=userinfo['last'], user=userinfo['user'])
	return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session.pop('token', None)
	return redirect(url_for('login'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='7001' ,debug = True)
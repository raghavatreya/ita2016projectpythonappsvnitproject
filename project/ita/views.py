from flask import Flask,render_template,session,redirect,url_for,request,flash
from app import app

@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/hello')
def hello():
	return "Hello World!"
	
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST': #do the login
		if request.form['username'] != 'sai' or request.form['password']!='123':
			error='Invalid credentials'
		else:
			flash('You have successfully logged in')
			session['logged_in']=True
			return redirect(url_for('index'))
		render_template('login.html',error=error)		
	else: #show login form
		return render_template('login.html')
	
@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You have successfully logged out')
	return redirect(url_for('index'))
	
@app.route('/user/<username>')
def show_user_profile(username):
	return 'User %s' % username	
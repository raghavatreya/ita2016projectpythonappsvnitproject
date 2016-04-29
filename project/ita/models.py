from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import datetime

db=SQLAlchemy()


class User(db.Model):
	__tablename__='users'
	uid=db.Column(db.Integer,primary_key=True)
	firstname=db.Column(db.String(100))
	lastname=db.Column(db.String(100))
	email=db.Column(db.String(100),unique=True)
	pwdhash=db.Column(db.String(20))

	def __init__(self,firstname,lastname,email,password):
		self.firstname=firstname
		self.lastname=lastname
		self.email=email
		self.set_password(password)

	def set_password(self,password):
		self.pwdhash=generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.pwdhash,password)

class Documents(db.Model):
	__tablename__='documents'
	#__searchable__ = ['docname']

	docid=db.Column(db.Integer,primary_key=True)
	docname=db.Column(db.String(200))
	docsize=db.Column(db.Integer)
	docpath=db.Column(db.String(500))
	docuploaddate=db.Column(db.DateTime,default=datetime.datetime.now())

	def __init__(self,docname,docsize,docpath):
		self.docname=docname
		self.docsize=docsize
		self.docpath=docpath

	def __repr__(self):
		return '<Name %r>' % (self.docname)	

	
class Docs(db.Model):
	__tablename__='docs'

	docid=db.Column(db.Integer,primary_key=True)
	docname=db.Column(db.String(200))
	filename=db.Column(db.String(500))
	author=db.Column(db.String(200))
	publisher=db.Column(db.String(200))
	tags=db.Column(db.String(200))
	docsize=db.Column(db.Integer)
	docpath=db.Column(db.String(500))
	imgpath=db.Column(db.String(500))
	uploaded=db.Column(db.DateTime,default=datetime.datetime.now())
	modified=db.Column(db.DateTime)

	def __init__(self,docname,filename,author,publisher,tags,docsize,docpath,imgpath):
		self.docname=docname
		self.filename=filename
		self.author=author
		self.publisher=publisher
		self.tags=tags
		self.docsize=docsize
		self.docpath=docpath
		self.imgpath=imgpath

	def __repr__(self):
		return '<Name %r>' % (self.docname)	


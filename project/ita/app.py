import os
from flask import Flask,render_template,session,redirect,url_for,request,flash,jsonify,send_from_directory
from models import db,User,Documents,Docs
from forms import SignupForm,SigninForm
from werkzeug import secure_filename
import flask.ext.whooshalchemy

app=Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #for sessions

UPLOAD_FOLDER = 'uploads/'
IMAGE_FOLDER='thumbnail_bucket'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sairam@localhost/ita' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER   # defining the upload folder
app.config['IMAGE_FOLDER']=IMAGE_FOLDER
app.config['WHOOSH_BASE'] = 'path/to/whoosh/base'

db.init_app(app)

@app.route('/')
def index():
	return render_template('landing.html')
	
@app.route('/hello')
def hello():
	return "Hello World!"
	
@app.route('/login',methods=['GET','POST'])
def login():
	form=SigninForm()

	if request.method=='POST': #do the login
		if form.validate()==False:
			return render_template('login.html',form=form)
		else:
			session['email']=form.email.data
			return redirect(url_for('home'))			
	else: #show login form
		return render_template('login.html',form=form)

@app.route('/home')
def home():
    return render_template('main.html') 

@app.route('/page')
def page():
    return render_template('dirPagination.tpl.html')           
	
@app.route('/logout')
def logout():
	session.pop('email',None)
	# flash('You have successfully logged out')
	return redirect(url_for('index'))

@app.route('/signup',methods=['GET','POST'])																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																															
def signup():
	form=SignupForm()

	if request.method=='POST':
		if form.validate() ==False:
			return render_template('signup.html',form=form)
		else:
			newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()
			redirect(url_for('login'))
			return jsonify({'status':201,'firstname':newuser.firstname,'lastname':newuser.lastname,'username':newuser.email,'message':"User successfully created"}),201,{'Location':url_for('')} #location : url for new created user                
			
	elif request.method=='GET':
		return render_template('signup.html',form=form)	

# @app.route('/signup1',methods=['GET','POST'])
# def sup():
#     if request.method=='POST':
#         if request.json:
#             json=request.json
#             print json
#             return jsonify(json)
#         else:
#             print "no json"    


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
    	resp={}
        file = request.files['file']
        docname=request.form['docname']
        author=request.form['author']
        publisher=request.form['publisher']
        tags=request.form['tags']


        if not file:
        	resp['status']=500
        	resp['message']='Internal Server Error'
        	return jsonify(resp)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            size=os.stat(path).st_size
            
            #save in database

            doc=Docs(docname,filename,author,publisher,tags,size,path,"")	
            db.session.add(doc)
            db.session.flush()
            did=doc.docid
            db.session.commit()


            #generating response
            resp['status']=200
            resp['file_name']=filename
            resp['id']=did
            resp['message']='file uploaded successfully'
        #    return redirect(url_for('uploaded_file',filename=filename))
            return jsonify(resp)
        else:
        	resp['status']=415
        	resp['message']='file type not supported'
        	return jsonify(resp)    
    return render_template('upload.html')

@app.route('/upload_image/<int:id>',methods=['POST'])
def upload_image(id):
    resp={}
    file = request.files['img']

    if not file:
        resp['status']=500
        resp['message']='Internal Server Error'
        return jsonify(resp)
    else:
        path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        #update in database
        doc=Docs.query.get(id)
        doc.imgpath=path
        doc.session.commit()    



    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename) 

@app.route('/delete/<int:id>')
def delete(id):
    resp={}
    doc=Docs.query.get(id)
    db.session.delete(doc)
    db.session.commit()
    resp["id"]=200
    resp["message"]="resource deleted successfully"
    return jsonify(resp)

@app.route('/update/<int:id>',methods=['POST','PUT'])
def update(id):
    if request.method=='POST':
        resp={}
        #get all data
        file = request.files['file']
        docname=request.form['docname']
        author=request.form['author']
        publisher=request.form['publisher']
        tags=request.form['tags']
        path=os.path.join(app.config['UPLOAD_FOLDER'], docname)
        file.save(path)
        size=os.stat(path).st_size
        
        #update database 
        doc=Docs.query.get(id)
        #db.session.delete(doc)

        doc.docname=docname
        doc.author=author
        doc.publisher=publisher
        doc.tags=tags
        doc.docsize=size
        doc.docpath=path

        db.session.commit()

        #generate response 
        resp["staus"]=200
        resp["message"]="updated successfully"
        return jsonify(resp)




@app.route('/display')
def display():
    resp={}
    docs=Docs.query.all()
    resp['docs']=[]
    for doc in docs:
        resp['docs'].append({'id':doc.docid,'name':doc.docname,'author':doc.author,'publisher':doc.publisher,'tags':doc.tags,'size':doc.docsize,'url':doc.docpath})
    return jsonify(resp)

@app.route('/search/<filename>')
def search(filename):
    doc=Documents.query.filter(Documents.docname.like("%"+filename+"%")).first()
   # doc=Documents.query.whoosh_search(filename).all()
    if doc is not None:
        resp={'status':200,'name':doc.docname,'size':doc.docsize,'url':doc.docpath}
    else:
        resp={'status':404,'message':'Document not found'}
    return jsonify(resp)       
	
	
if __name__=='__main__':
	app.run(debug=True)	

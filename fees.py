from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kgisl@localhost/fees'
app.config['SECRET_KEY'] = "random string"


db = SQLAlchemy(app)
                                                                                         

@app.route('/')
def Home():
  return render_template('login.html') 

  
@app.route('/logout')
def logout():
    return redirect(url_for('Home'))  
    
class student_detail(db.Model):
	id = db.Column('student_id', db.Integer, primary_key = True )
	stu_name = db.Column(db.String(50),unique=True)
	college = db.Column(db.String(200)) 
	degree = db.Column(db.String(10))
	year_of_study = db.Column(db.Integer)
	phone_number = db.Column(db.Integer,unique=True)
	email_id = db.Column(db.String(50),unique=True)
	course = db.Column(db.String(20))
	course_fees= db.Column(db.Integer)
	total_fees= db.Column(db.Integer)
	type_of_training = db.Column(db.String(20))
	active= db.Column(db.Integer,default=1)


	
	def __init__(self, stu_name, college, degree,year_of_study,phone_number,email_id,course,course_fees,total_fees,type_of_training,active):
		self.stu_name = stu_name
		self.college = college
		self.degree = degree
		self.year_of_study = year_of_study
		self.phone_number = phone_number
		self.email_id = email_id
		self.course = course
		self.course_fees = course_fees
		self.total_fees= total_fees
		self.type_of_training = type_of_training
		self.active= active
	
	@app.route('/db')
	def show_all():
		return render_template('add_student.html', student_detail = student_detail.query.filter_by(active=1).all() )
		
	@app.route('/new', methods = ['GET', 'POST'])
	def new():
		if request.method == 'POST':
			if  not request.form['stu_name'] or not request.form['college'] or not request.form['degree'] or not request.form['year_of_study'] or not request.form['phone_number']  or not request.form['email_id'] or not request.form['course'] or not request.form['course_fees'] or not request.form['total_fees']or not request.form['type_of_training'] or not request.form['active']:
				flash('Please enter all the fields', 'error')
			else:
				student = student_detail( request.form['stu_name'],
					request.form['college'], request.form['degree'], request.form['year_of_study'], request.form['phone_number'], request.form['email_id'], request.form['course'], request.form['course_fees'], request.form['total_fees'] ,request.form['type_of_training'],request.form['active'])
                
				db.session.add(student)
				db.session.commit()
				flash('Record was successfully added')
			return redirect(url_for('show_all'))
		return render_template('add_student.html')
		
	@app.route('/edit/<id>', methods = ['GET' , 'POST'])
	def edit(id):
		student= student_detail.query.get(id)
		if request.method == 'POST':
			student.stu_name = request.form['stu_name']
			student.college = request.form['college']
			student.degree=request.form['degree']
			student.year_of_study=request.form['year_of_study']
			student.phone_number=request.form['phone_number']
			student.email_id=request.form['email_id']
			student.course=request.form['course']
			student.course_fees=request.form['course_fees']
			student.total_fees=request.form['total_fees']
			student.type_of_training=request.form['type_of_training']
			student.active=request.form['active']
			db.session.commit()
			return redirect(url_for('show_all'))
		return render_template('edit.html',student=student)

	@app.route('/status/<id>',methods=['GET','POST'])
	def status(id):
		student = student_detail.query.get(id)	
		student.active =0
		db.session.commit()
		return redirect(url_for('show_all'))
	       
	
	"""@app.route('/post_delete/<id>' , methods=['POST', 'GET'])
	def post_delete (id):
		student = student_detail.query.get(id)
		if student == None:
			flash("This entry does not exist in the database")
			return redirect(url_for(show_all))
		post_delete=student.delete(student)
		if not post_delete:
			flash("Post was deleted successfully")
		else:
			error=post_delete
			flash(error)
		return redirect(url_for('show_all'))"""
 
		
class course_enquiry(db.Model):
	id = db.Column('stu_enquiry_id', db.Integer, primary_key = True )
	stu_name = db.Column(db.String(50),unique=True)
	college = db.Column(db.String(200)) 
	degree = db.Column(db.String(10))
	phone_number = db.Column(db.Integer,unique=True)
	email_id = db.Column(db.String(50),unique=True)
	date_of_enquiry=db.Column(db.Date)
	active= db.Column(db.Integer,default=1)
	
	def __init__(self, stu_name, college, degree,phone_number,email_id,date_of_enquiry,active):
		self.stu_name = stu_name
		self.college = college
		self.degree = degree
		self.phone_number = phone_number
		self.email_id = email_id
		self.date_of_enquiry = date_of_enquiry
		self.active=active
		
	
	@app.route('/db_course_enquiry')
	def course_enquiry():
		return render_template('add_course_enquiry.html', course_enquiry =course_enquiry.query.filter_by(active=1).all() )
		
	@app.route('/new_course_enquiry', methods = ['GET', 'POST'])
	def new_course_enquiry():
		if request.method == 'POST':
			if not request.form['stu_name'] or not request.form['college'] or not request.form['degree'] or not request.form['phone_number'] or not request.form['email_id'] or not request.form['date_of_enquiry']or not request.form['active']:
				flash('Please enter all the fields', 'error')
			else:
				stu_enquiry = course_enquiry( request.form['stu_name'],
					request.form['college'], request.form['degree'],  request.form['phone_number'],  request.form['email_id'], request.form['date_of_enquiry'], request.form['active'])
                
				db.session.add(stu_enquiry)
				db.session.commit()
				flash('Record was successfully added')
			return redirect(url_for('course_enquiry'))
		return render_template('add_course_enquiry.html')
		
	@app.route('/edit_course_enquiry/<id>', methods = ['GET' , 'POST'])
	def edit_course_enquiry(id):
		stu_enquiry= course_enquiry.query.get(id)
		if request.method == 'POST':
			stu_enquiry.stu_name = request.form['stu_name']
			stu_enquiry.college = request.form['college']
			stu_enquiry.degree=request.form['degree']
			stu_enquiry.phone_number=request.form['phone_number']
			stu_enquiry.email_id=request.form['email_id']
			stu_enquiry.date_of_enquiry=request.form['date_of_enquiry']
			stu_enquiry.active=request.form['active']
			db.session.commit()
			return redirect(url_for('course_enquiry'))
		return render_template('edit_course_enquiry.html',stu_enquiry=stu_enquiry)
	
	@app.route('/status_course_enquiry/<id>' , methods=['POST', 'GET'])
	def status_course_enquiry(id):
		stu_enquiry=course_enquiry.query.get(id)
		stu_enquiry.active = 0
		db.session.commit()
		return redirect(url_for('course_enquiry'))	

class workshop_details(db.Model):
	id = db.Column('workshops_id', db.Integer, primary_key = True )
	topic= db.Column(db.String(50))
	num_of_days = db.Column(db.Integer)
	from_date = db.Column(db.Date()) 
	to_date = db.Column(db.Date()) 
	handle_engg = db.Column(db.String(50))
	num_engg = db.Column(db.Integer)
	num_participants = db.Column(db.Integer)
	active= db.Column(db.Integer,default=1)
	
	
	def __init__(self,topic,num_of_days,from_date,to_date,handle_engg,num_engg ,num_participants,active):
		self.topic = topic
		self. num_of_days =  num_of_days
		self.from_date = from_date
		self.to_date = to_date
		self.handle_engg= handle_engg
		self.num_engg = num_engg
		self.num_participants = num_participants
		self.active=active
		
	
	@app.route('/db_workshop')
	def workshop():
		return render_template('add_workshop.html', workshop_details=workshop_details.query.filter_by(active=1).all() )
		
	@app.route('/new_workshop', methods = ['GET', 'POST'])
	def new_workshop():
		if request.method == 'POST':
			if not request.form['topic'] or not request.form['num_of_days'] or not request.form['from_date'] or not request.form['to_date'] or not request.form['handle_engg'] or not request.form['num_engg'] or not request.form['num_participants']or not request.form['active']:
				flash('Please enter all the fields', 'error')
			else:
				workshops = workshop_details(request.form['topic'], request.form['num_of_days'],
					request.form['from_date'], request.form['to_date'], request.form['handle_engg'],  request.form['num_engg'],  request.form['num_participants'],  request.form['active'])
                
				db.session.add(workshops)
				db.session.commit()
				flash('Record was successfully added')
			return redirect(url_for('workshop'))
		return render_template('add_workshop.html')
		
	@app.route('/edit_workshop/<id>', methods = ['GET' , 'POST'])
	def edit_workshop(id):
		workshops = workshop_details.query.get(id)
		if request.method == 'POST':
			workshops .topic=request.form['topic']
			workshops .num_of_days = request.form['num_of_days']
			workshops .from_date = request.form['from_date']
			workshops .to_date = request.form['to_date']
			workshops .handle_engg=request.form['handle_engg']
			workshops .num_engg=request.form['num_engg']
			workshops .num_participants=request.form['num_participants']
			workshops .active=request.form['active']
			db.session.commit()
			return redirect(url_for('workshop'))
		return render_template('edit_workshop.html',workshops=workshops)
	
	@app.route('/status_workshops/<id>' , methods=['POST', 'GET'])
	def status_workshops(id):
		workshops=workshop_details.query.get(id)
		workshops.active = 0
		db.session.commit()
		return redirect(url_for('workshop'))
        
		
if __name__ == '__main__':
   db.create_all()
   app.run(debug=True)




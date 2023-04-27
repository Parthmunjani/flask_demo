from flask import  Flask,Blueprint,jsonify,make_response,request
from flask_restful import Resource,abort,marshal_with,fields
from model import ShowData,db,Modification,Student,School
#from db import method
from datetime import datetime

class AllDataView(Resource):
    def get(self):
        try:
            tasks = ShowData.query.all()
            if not tasks:
                return make_response({"status":False,"detail":"No Data In Table"})
            data = [task.to_json(task) for task in tasks]
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def post(self):
        try:
            data=request.get_json()
            create_data = ShowData(data)
            ShowData.add(create_data)
            data=create_data.to_json(create_data)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})

    def delete(self):
        try:
            task = ShowData.query.all()
            ShowData.delete(task)
            return make_response({"Status":True,"detail":"Data Delete"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
class OneDataView(Resource):
    def get(self,id):
        try:
            task = ShowData.query.filter_by(nid=id).first() 
            data=task.to_json(task)
            return make_response({"status":True,"detail":data})
        except:
            return make_response({"status":False,"detail":"Could not find task with that id "})
        
    def put(self,id):
        try:
            data=request.get_json()
            task = ShowData.query.filter_by(nid=id).first()
            if not task:
                abort(404,message="task doesn't exist,cannot update")
            task.task = data.get('task')
            task.summary = data.get('summary')
            ShowData.put()
            data=task.to_json(task)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
         
    def delete(self,id):
        try:
            task = ShowData.query.get_or_404(id)
            ShowData.delete(task)
            return make_response({"Status":True,"detail":"Data Delete"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
class StudentView(Resource):
    def get(self):
        try:
            tasks =Student.query.all()
            if not tasks:
                return make_response({"status":False,"detail":"No Student Data In Table"})
            data = [task.to_json(task) for task in tasks]
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})

    def post(self):
        try:
            data=request.get_json()
            create_data = Student(data)
            Student.add(create_data)
            data=create_data.to_json(create_data)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
class StudentDetail(Resource):
    def get(self,id):
        try:
            student_data = Student.query.filter_by(id=id).first() 
            data=student_data.to_json(student_data)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def put(self,id):
        try:
            data=request.get_json()
            student_data = Student.query.filter_by(id=id).first()
            if not student_data:
                abort(404,message="Student doesn't exist,cannot update")
            student_data.name = data.get('name')
            student_data.school_id = data.get('school_id')
            student_data.modified_at=datetime.utcnow()
            Student.put()
            data=student_data.to_json(student_data)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def delete(self,id):
        try:
            student_data = Student.query.get_or_404(id)
            Student.delete(student_data)
            return make_response({"Status":True,"detail":"Student Delete"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
class SchoolView(Resource):
    def get(self):
        try:
            school_data =School.query.all()
            if not school_data:
                return make_response({"status":False,"detail":"No School Data In Table"})
            data = [task.to_json(task) for task in school_data]
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def post(self):
        try:
            data=request.get_json()
            create_data = School(data)
            School.add(create_data)
            data=create_data.to_json(create_data)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
class SchoolDetail(Resource):
    def get(self,id):
        try:
            school_data = School.query.filter_by(id=id).first() 
            data=school_data.to_json(school_data)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def put(self,id):
        try:
            data=request.get_json()
            school_data = School.query.filter_by(id=id).first()
            if not school_data:
                abort(404,message="Student doesn't exist,cannot update")
            school_data.name = data.get('name')
            school_data.modified_at=datetime.utcnow()
            School.put()
            data=school_data.to_json(school_data)
            return make_response({"status":True,"detail":data})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})
        
    def delete(self,id):
        try:
            school_data = School.query.get_or_404(id)
            School.delete(school_data)
            return make_response({"Status":True,"detail":"Student Delete"})
        except Exception as e:
            return make_response({"status":False,"detail":str(e)})    
        
class SchoolStudent(Resource):
    def get(self,school_id):
        try:
            print(school_id)
            school=School.query.get_or_404(school_id)
            if not school:
                return make_response({"status":False,"details":"This School Not Registered"})
            students=[student.name for student in school.students]
            return make_response({"status":True,"detail":students})
        except Exception as e:
            return make_response({"status":False,"details":str(e)})
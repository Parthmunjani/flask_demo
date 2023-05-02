from flask import  Flask,Blueprint,jsonify,make_response,request
from flask_restful import Resource,abort,marshal_with,fields
from model import ShowData,db,Modification,Student,School
#from db import method
from datetime import datetime
import logging
import time

#Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create a file handler
handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        response = func(*args, **kwargs)
        end_time = time.monotonic()
        logger.info(f'{func.__name__} took {end_time - start_time:.6f} seconds')
        return response
    return wrapper

class AllDataView(Resource):
    @measure_time
    def get(self):
        try:
            tasks = ShowData.query.all()
            if not tasks:
                return make_response({"status":False,"detail":"No Data In Table"})
            data = [task.to_json(task) for task in tasks]
            logger.info('Get Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
    @measure_time    
    def post(self):
        try:
            data=request.get_json()
            create_data = ShowData(data)
            ShowData.add(create_data)
            data=create_data.to_json(create_data)
            logger.info('POST Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
    @measure_time
    def delete(self):
        try:
            task = ShowData.query.all()
            ShowData.delete(task)
            logger.info('Delete Request Received')
            return make_response({"Status":True,"detail":"Data Delete"})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
class OneDataView(Resource):
    @measure_time
    def get(self,id):
        try:
            task = ShowData.query.filter_by(nid=id).first() 
            data=task.to_json(task)
            logger.info('Get Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
    
    @measure_time    
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
            logger.info('PUT Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
    
    @measure_time     
    def delete(self,id):
        try:
            task = ShowData.query.get_or_404(id)
            ShowData.delete(task)
            logger.info('DELETE Request Received')
            return make_response({"Status":True,"detail":"Data Delete"})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
class StudentView(Resource):
    @measure_time
    def get(self):
        try:
            tasks =Student.query.all()
            if not tasks:
                return make_response({"status":False,"detail":"No Student Data In Table"})
            data = [task.to_json(task) for task in tasks]
            logger.info('Get Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
    @measure_time
    def post(self):
        try:
            data=request.get_json()
            create_data = Student(data)
            Student.add(create_data)
            data=create_data.to_json(create_data)
            logger.info('POST Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
class StudentDetail(Resource):
    @measure_time
    def get(self,id):
        try:
            student_data = Student.query.filter_by(id=id).first() 
            data=student_data.to_json(student_data)
            logger.info('Get Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
    @measure_time    
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
            logger.info('PUT Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
       
    @measure_time   
    def delete(self,id):
        try:
            student_data = Student.query.get_or_404(id)
            Student.delete(student_data)
            logger.info('DELETE Request Received')
            return make_response({"Status":True,"detail":"Student Delete"})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
class SchoolView(Resource):
    @measure_time
    def get(self):
        try:
            school_data =School.query.all()
            if not school_data:
                return make_response({"status":False,"detail":"No School Data In Table"})
            data = [task.to_json(task) for task in school_data]
            logger.info('Get Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
    
    @measure_time    
    def post(self):
        try:
            data=request.get_json()
            create_data = School(data)
            School.add(create_data)
            data=create_data.to_json(create_data)
            logger.info('POST Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
class SchoolDetail(Resource):
    @measure_time
    def get(self,id):
        try:
           # print(id)
            school=School.query.get_or_404(id)
            if not school:
                return make_response({"status":False,"details":"This School Not Registered"})
            students=[student.name for student in school.students]
            logger.info('%s Get Request Received',students)
            return make_response({"status":True,"detail":students})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"details":str(e)})
     
    @measure_time    
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
            logger.info('PUT Request Received')
            return make_response({"status":True,"detail":data})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})
        
    @measure_time    
    def delete(self,id):
        try:
            school_data = School.query.get_or_404(id)
            School.delete(school_data)
            logger.info('DELETE Request Received')
            return make_response({"Status":True,"detail":"Student Delete"})
        except Exception as e:
            logger.error("%s",e)
            return make_response({"status":False,"detail":str(e)})    
            
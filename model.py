from flask import Flask,jsonify,request
from flask_restful import Resource,Api,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4

db=SQLAlchemy()

class Modification:
    
    def delete(instance):
        db.session.delete(instance)
        db.session.commit() 
        
    def add(instance):
        db.session.add(instance)
        db.session.commit()    
        
    def put():
        db.session.commit()
        
class ShowData(db.Model,Modification):
    nid=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200))
    summary=db.Column(db.String(200))   
    
    def to_json(self, data):
        data={"id":data.nid,"task":data.task,"summary":data.summary}
        return data
        
    def __init__(self,data):  
        self.nid=data.get('id')
        self.task=data.get('task')
        self.summary=data.get('summary')
        
class Student(db.Model,Modification):
    __tablename__ = "student"
     
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    uuid = db.Column(db.String(36),nullable=False, default=str(uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_at=db.Column(db.DateTime,default=datetime.utcnow)
    is_deleted=db.Column(db.Boolean,default=False)
    school_id=db.Column(db.Integer,db.ForeignKey('school.id'))
    
    def __init__(self,data):
        self.name=data.get('name')
        self.school_id=data.get('school_id')
        
    def to_json(self, data):
        data={"id":data.id,"name":data.name,"school_id":data.school_id}
        return data
      
class School(db.Model,Modification):
    __tablename__="school"
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    modified_at=db.Column(db.DateTime,default=datetime.utcnow)
    is_deleted=db.Column(db.Boolean,default=False)
    students=db.relationship('Student', backref='school')
    
    def __init__(self,data):
        self.name=data.get('name')
        
    def to_json(self,data):
        data={"id":data.id,"name":data.name}
        return data
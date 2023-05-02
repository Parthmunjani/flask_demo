from flask import Blueprint, Flask,jsonify,request
from flask_restful import Resource,Api,reqparse,abort
from blueprint.app2 import AllDataView,OneDataView,StudentView,StudentDetail,SchoolView,SchoolDetail
from flask_migrate import Migrate
import logging
# from blueprint.app2 import dataCtrlr

from model import db
from api import Show,Index

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///instance/sqlite.db'
    

db.init_app(app)
migrate=Migrate(app,db)

"""with app.app_context():
    db.create_all()"""


data_blueprint=Blueprint('data', __name__)

api=Api(data_blueprint)
app.register_blueprint(data_blueprint, url_prefix='/')

api.add_resource(Index,'/'),
api.add_resource(Show,'/home')
api.add_resource(AllDataView,'/get_data/')
api.add_resource(OneDataView,'/get_data/<int:id>')
api.add_resource(StudentView,'/student')
api.add_resource(StudentDetail,'/student/<int:id>')
api.add_resource(SchoolView,'/school')
api.add_resource(SchoolDetail,'/school/<int:id>')


if __name__=='__main__':
    app.run(debug=True, port=3000)
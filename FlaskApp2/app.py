from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from model.Student_Model import StudentModel,db
# from Student_app import app
from flask_cors import CORS
from config.settings import *
from routes.Student_app import *

db.init_app(app)

if __name__ == '__main__':

    db.create_all()
    app.run(debug=True)
    
    
    











# app = Flask(__name__)
# CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False






















# from importlib.resources import Resource
# from sqlite3 import apilevel
# from flask import Flask, jsonify, render_template, request, url_for
# from flask_restful import Api, Resource, reqparse
# from flask_sqlalchemy import SQLAlchemy
# from models import StudentModel,db
# app = Flask(__name__)
# from flask_cors import CORS

# CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    
# api = Api(app)
# db.init_app(app)

# @app.before_request
# def create_table():
#       db.create_all()
    


# with app.app_context():
    
    # db.create_all()
    

# class StudentData(Resource):
    
#     def get(self):
#         students = StudentModel.query.all()
#         return {'Students' : list(x.json() for x in students)}
        
#     def post(self):
#         data = request.get_json()
#         new_student = StudentModel(id=data['id'],name=data['name'],email=data['email'],gender=data['gender'])
#         db.session.add(new_student)
#         db.session.commit()
#         db.session.flush()
#         print(db.id)
#         return new_student.json(),201
    
# class SingleStudentView(Resource):
#     def get(self,id):
#         student = StudentModel.query.filter_by(id=id).first()
#         if student:
#             return student.json()
#         return {'message': 'Student id not found'},404
    
#     def delete(self,id):
#         student = StudentModel.query.filter_by(id=id).first()
#         if student:
#             db.session.delete(student)
#             db.session.commit()
#             return {"message":'deleted'}
#         else:
#             return {'message': 'Student id not found'},404
        
#     def put(self,id):
#         data = request.get_json()
#         student = StudentModel.query.filter_by(id=id).first()
#         if student:
#             student.id = data["id"]
#             student.name = data["name"]
#             student.email = data["email"]
#             student.gender = data["gender"]
#         else:
#             student = StudentModel(id=id,**data)
            
#         db.session.add(student)
#         db.session.commit()
#         return student.json()
    
   

    
# api.add_resource(StudentData,'/students')
# api.add_resource(SingleStudentView,'/student/<int:id>')
# @app.route('/students/<int:id', methods=['GET', 'POST', 'DELETE', 'UPDATE'])
# def home():
#     student = StudentModel.query.all()
#     return render_template(student=student)


# # @app.route('/student/<int:id>', methods=['GET'])

# app.debug= True
# if __name__ == '__main__':
#     app.run(host= 'localhost', port=5000,use_reloader=False)





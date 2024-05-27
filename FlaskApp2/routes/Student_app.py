from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from model.Student_Model import StudentModel, add_students,db, delete_student, edit_student, singleStudentById, single_student, students
from config.settings import *
# app = Flask(__name__)

@app.route('/students', methods=['GET'])
def student():
    return students()
    
@app.route('/students', methods=['POST'])
def add_stud():
    return add_students()
    

@app.route('/students/<string:email>', methods=['GET'])
def get_stud(email):
    return single_student(email)

@app.route('/students/<int:id>', methods=['GET'])
def get_studById(id):
    return singleStudentById(id)


@app.route('/students/<int:id>', methods=['PUT'])
def update(id):
    return edit_student(id)
    
@app.route('/students/<int:id>', methods=['DELETE'])
def delete(id):
    return delete_student(id)

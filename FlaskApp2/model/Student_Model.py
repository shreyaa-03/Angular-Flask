from http.client import  HTTPException
from sqlite3 import DataError, IntegrityError, OperationalError
from flask import app
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound, IntegrityError
from werkzeug.exceptions import HTTPException, BadRequest, RequestTimeout, InternalServerError
from sqlalchemy import text
from config.settings import *
import re
from email_validator import validate_email, EmailNotValidError



db = SQLAlchemy()

class StudentModel(db.Model):
    ___tablename___ = 'students'
    id = db.Column(db.Integer(), primary_key = True, autoincrement = True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique = True)
    gender = db.Column(db.String(80))
    
    def __init__(self, name, email,gender):
        # self.id = id
        self.name = name
        self.email = email
        self.gender = gender
        
    def json(self):
        return {"id": self.id, "name": self.name, "email": self.email, "gender": self.gender}
    
    
    def createResponse(status_code, error_message):
        response = {
        "status": "error",
        "message": error_message
    }
        return jsonify(response), status_code
    
# @app.route('/students', methods=['GET'])
def students():
    try:
        students = StudentModel.query.all()
       
        if students is None:
            raise NoResultFound()
        return jsonify([student.json() for student in students])

    except NoResultFound as e:
        # return jsonify({"error": "No students found in the databse" + str(e)}),
        return createResponse(404, "No students found in the database.")
    except OperationalError as e:
        # return jsonify({"error": "Database server is not running or is inaccessible. "  + str(e) }), 400
         return createResponse(500, "Database server is not running or is inaccessible: " + str(e))
    except InternalServerError as e:
        return createResponse(500, "Internal Server Error: " + str(e))
    except HTTPException as e:
        return createResponse( str(e) )
    except Exception as e:
        return createResponse( {str(e)})
    
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "The requested URL was not found on the server. If you entered the URL manually, please check your spelling and try again."}), 404
 

# @app.route('/students', methods=['POST'])
def add_students():
    try:
        data = request.get_json()
        name = request.json['name']
        email = data.get('email')
        # gender = data.get('gender')
        gender_flag = data.get('gender')
        
        if not validate_email(email):
            raise ValueError("Invalid email format")
        
        if not isinstance(name, str):
            raise ValueError('Invalid data type. Please enter a string.')
        
        gender_mapping = {
            'm': 'male',
            'f': 'female',
            'o': 'other'
        }
        gender_string = gender_mapping.get(gender_flag)

        # Validate gender
        if gender_string not in ['male', 'female', 'other']:
            raise ValueError('Please select either male,female, or other as the gender')

        new_student = StudentModel( name=data['name'], email=data['email'], gender=gender_string)
        db.session.add(new_student)
        db.session.commit()
        return createResponse( 201,new_student.json(), "Student added successfully")
    except EmailNotValidError as e:
       return  createResponse( str(e))
    except IntegrityError:  
        return createResponse(400,"Email Id already exists, use another email id to add new student")
    except ValueError as e:
        return createResponse(400,str(e))
        # return jsonify({"error: ": "Invalid data type. Please enter a string."})
    except KeyError as e:
        # return jsonify({"error": "Missing required field: " + str(e.args[0])}), 400
        return createResponse(400, "Missing required field: {e.args[0]}")
    except OperationalError as e:
        return createResponse(500,"Database operational error: "  + str(e))
     
    except InternalServerError as e:
        return createResponse(500,"Internal Server Error: " + str(e))
    except HTTPException as e:
        return createResponse(404,"Page not found: " + str(e))




# @app.route('/students/<int:id>', methods=['GET'])
def single_student(email_or_name):
    try:
        # student = StudentModel.query.get(email)
        # student = StudentModel.query.filter_by(email=email_or_name).first()
        
        # If not an email, assume it's a name
        # if student is None:
        #     student = StudentModel.query.filter_by(name=email_or_name).first()
        search_by_email = False
        search_by_name = False
  

        # if email_or_name.isdigit():
        #     search_by_id = True
        if '@' in email_or_name:
            search_by_email = True
        else:
            search_by_name = True

        query = None

        if search_by_email:
            query = StudentModel.query.filter_by(email=email_or_name)
        elif search_by_name:
            query = StudentModel.query.filter_by(name=email_or_name)
        # elif search_by_id:
        #     query = StudentModel.query.filter_by(id=email_or_name)

        student = query.first()
        
        
        if student is None:
            raise NoResultFound()
        # if student:
        return jsonify(student.json())
    except NoResultFound as e:
        # return jsonify({"error": "No students found in the databse" + str(e)}),
        return createResponse(404, "No students found in the database.")
    except OperationalError as e:
        # return jsonify({"error": "Database server is not running or is inaccessible. "  + str(e) }), 400
         return createResponse(500, "Database server is not running or is inaccessible: " + str(e))
    except InternalServerError as e:
        return createResponse(500, "Internal Server Error: " + str(e))
    except HTTPException as e:
        return createResponse( str(e) )
    except Exception as e:
        return createResponse( {str(e)})
   
    

def singleStudentById(id):
    
    try:
        student = StudentModel.query.get(id)
        if student is None:
            raise NoResultFound()
        # if student:
        return jsonify(student.json())
    
    except NoResultFound as e:
        # return jsonify({"error": "No students found in the databse" + str(e)}),
        return createResponse(404, "No students found in the database.")
    except OperationalError as e:
        # return jsonify({"error": "Database server is not running or is inaccessible. "  + str(e) }), 400
         return createResponse(500, "Database server is not running or is inaccessible: " + str(e))
    except InternalServerError as e:
        return createResponse(500, "Internal Server Error: " + str(e))
    except HTTPException as e:
        return createResponse( str(e) )
    except Exception as e:
        return createResponse( {str(e)})

    
# @app.route('/students/<int:id>', methods=['PUT'])
def edit_student(id): 
# def edit_student(email_or_name): 
    try:
        
        student = StudentModel.query.get(id)
       
        # student = StudentModel.query.filter_by(email=email_or_name).first()
        
        # If not an email, assume it's a name
        # if student is None:
            # student = StudentModel.query.filter_by(name=email_or_name).first()
        
        if student is None:
            raise NoResultFound()
        
        
        data = request.get_json()
        if 'email' in data and data['email'] != student.email:
            return jsonify({"error": "Email ID cannot be modified. Student not updated"}), 400
        name = request.json['name']
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        student.name = data["name"]
        # student.email = data["email"]
        student.gender = data["gender"]
        db.session.commit()
        
        return createResponse(student.json(),"Student updated successfully!")
        
    except NoResultFound as e:
        # return jsonify({"error": "No students found in the databse" + str(e)}),
        return createResponse(404, "No students found in the database.")
    except OperationalError as e:
        # return jsonify({"error": "Database server is not running or is inaccessible. "  + str(e) }), 400
         return createResponse(500, "Database server is not running or is inaccessible: " + str(e))
    except InternalServerError as e:
        return createResponse(500, "Internal Server Error: " + str(e))
    except HTTPException as e:
        return createResponse( str(e) )
    except Exception as e:
        return createResponse( {str(e)})
    
    
# @app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        # student = StudentModel.query.filter_by(email=email_or_name).first()
        
        # If not an email, assume it's a name
        # if student is None:
            # student = StudentModel.query.filter_by(name=email_or_name).first()
        student = StudentModel.query.get(id)
        if student is None:
            raise NoResultFound()
        db.session.delete(student)
        db.session.commit()
        return createResponse(200, 'Student deleted successfully')
    except NoResultFound as e:
        # return jsonify({"error": "No students found in the databse" + str(e)}),
        return createResponse(404, "No students found in the database.")
    except OperationalError as e:
        # return jsonify({"error": "Database server is not running or is inaccessible. "  + str(e) }), 400
         return createResponse(500, "Database server is not running or is inaccessible: " + str(e))
    except InternalServerError as e:
        return createResponse(500, "Internal Server Error: " + str(e))
    except HTTPException as e:
        return createResponse( str(e) )
    except Exception as e:
        return createResponse( {str(e)})
    
@app.errorhandler(404)
def not_found_error(error):
    return create_error_response(404, "The requested URL was not found on the server. If you entered the URL manually, please check your spelling and try again.")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # except NoResultFound:
    #     return jsonify({'error': 'Student not found in the database'}), 404
    # except ValueError:
    #     return jsonify({"error": 'Invalid ID provided'}), 400
    # except InternalServerError as e: 
    #     return jsonify({"error": "Internal Server Error: " + str(e)}), 500
    # except HTTPException as e:
    #     return jsonify({"error": "Page not found: " + str(e)})
    # except OperationalError as e:
    #     return jsonify({"error": "Database operational error: " + {str(e)}}), 500 
    # except Exception as e:
    #     return jsonify({"error: " +  str(e)}), 500
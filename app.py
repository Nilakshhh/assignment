from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from models.employee import Employee
from models.tokenValidation import TokenValidation
from models.tokenGenerator import TokenGenerator
from models.empOperations import EmployeeOperations
import jwt
import datetime
from config import Config
import json

app = Flask(__name__)
secret_key = Config.SECRET_KEY

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/profile')
def profile():
    token = request.cookies.get('token')
    if token is None:
        return redirect('/')

    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    role = payload.get('role')
    return render_template('profile.html', role=role)

@app.route('/add')
def add():
    token = request.cookies.get('token')
    token_validator = TokenValidation(token)
    token_validation_score = token_validator.get_token_score()
    
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    role = payload.get('role')

    if token_validation_score < 2:
        return render_template('404.html', message = "You are not allowed to access this functionality.")
    else:
        return render_template('add.html', role = role)

@app.route('/admin')
def admin():
    token = request.cookies.get('token')
    token_validator = TokenValidation(token)
    token_validation_score = token_validator.get_token_score()

    if token_validation_score < 3:
        return render_template('404.html', message = "You are not allowed to access this functionality.")
    else:
        return render_template('admin.html')

@app.route('/api/auth/login', methods = ["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if not email or not password:
        return 'Missing email or password', 400

    employee = Employee(email, password, role)
    login_status = json.loads(employee.authenticate())

    if login_status['authenticated']:
        token_generator = TokenGenerator(employee)
        token = token_generator.generate_token()

        response = make_response(redirect(url_for('profile')))

        response.set_cookie('token', token)
        return response
    else:
        return render_template('login_error.html', message = login_status['message'])


    return jsonify({'message': 'Invalid login procedure'}), 401

@app.route('/api/employees', methods=['POST', 'GET'])
def employeeOps():
    token = request.cookies.get('token')
    token_validator = TokenValidation(token)
    token_validation_score = token_validator.get_token_score()
    
    if token_validation_score == 0:
        return render_template('404.html', message = "Token expired, please log-in again")
    
    employeeOperation = EmployeeOperations()

    if request.method == 'GET':
        employees = employeeOperation.view_all()
        return jsonify(employees)

    if request.method == 'POST' and token_validation_score > 1:
        employee_data = request.json
        email = employee_data.get('email')
        password = employee_data.get('password')
        role = employee_data.get('role')
        
        response, status_code = employeeOperation.add_user(email, password, role)
    
        if status_code == 200:  # Successful addition of user
            return jsonify({"message": response})
        elif status_code == 409:  # Conflict, user with email already exists
            return jsonify({"error": response}), 409
        else:
            return jsonify({"error": response}), 500  # Internal Server Error
    else:
        return render_template('404.html', message="You are not allowed to access this functionality.")


@app.route('/api/employees/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def employeeOpsWithId(id):
    token = request.cookies.get('token')
    token_validator = TokenValidation(token)
    token_validation_score = token_validator.get_token_score()

    if token_validation_score == 0:
        return jsonify({"error": "Invalid token, Please Login again"}), 401
    
    employeeOperation = EmployeeOperations(id)

    if request.method == 'GET':
        employee = employeeOperation.view_emp()
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        return jsonify(employee)

    if request.method == 'PUT' and token_validation_score > 1:
        data = request.json
        response = employeeOperation.update_emp(data)
        return jsonify(response)
    else:
        return render_template('404.html', message = "You are not allowed to access this functionality.")

    if request.method == 'DELETE' and token_validation_score > 2:
        response = employeeOperation.delete_emp()
        return jsonify(response)
    else:
        return render_template('404.html', message = "You are not allowed to access this functionality.")

@app.route('/logout', methods=['POST'])
def logout():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

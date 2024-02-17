from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
from models.employee import Employee
from models.tokenValidation import TokenValidation
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
    tokenValidator = TokenValidation(token)
    tokenValidationScore = tokenValidator.get_token_score()
    
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    role = payload.get('role')

    if tokenValidationScore < 2:
        return render_template('404.html', message = "You are not allowed to access this functionality.")
    else:
        return render_template('add.html', role = role)

@app.route('/admin')
def admin():
    token = request.cookies.get('token')
    tokenValidator = TokenValidation(token)
    tokenValidationScore = tokenValidator.get_token_score()

    if tokenValidationScore < 3:
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
    login_status = json.loads(employee.authenticate(email, password, role))
    print(login_status)

    if login_status['authenticated']:
        current_time = datetime.datetime.utcnow()
        current_time_str = current_time.isoformat()

        expiration_time = current_time + datetime.timedelta(minutes=600)
        expiration_time_str = expiration_time.isoformat()

        payload = {"email": email, "role": role, "login_time": current_time_str, "expiration_time": expiration_time_str}

        token = jwt.encode(payload, secret_key, algorithm="HS256")
        response = make_response(redirect(url_for('profile')))

        response.set_cookie('token', token)
        return response
    else:
        return render_template('login_error.html', message = login_status['message'])


    return jsonify({'message': 'Invalid login procedure'}), 401

@app.route('/api/employees', methods=['POST', 'GET'])
def employeeOps():
    token = request.cookies.get('token')
    tokenValidator = TokenValidation(token)
    tokenValidationScore = tokenValidator.get_token_score()
    
    if tokenValidationScore == 0:
        return render_template('404.html', message = "Token expired, please log-in again")
    
    employeeOperation = EmployeeOperations()

    if request.method == 'GET':
        employees = employeeOperation.view_all()
        return jsonify(employees)

    if request.method == 'POST' and tokenValidationScore > 1:
        employee_data = request.json
        email = employee_data.get('email')
        password = employee_data.get('password')
        role = employee_data.get('role')
        
        response = employeeOperation.add_user(email, password, role)
        
        return jsonify({"message": "Employee data received successfully"})
    else:
        return render_template('404.html', message = "You are not allowed to access this functionality.")


@app.route('/api/employees/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def employeeOpsWithId(id):
    token = request.cookies.get('token')
    tokenValidator = TokenValidation(token)
    tokenValidationScore = tokenValidator.get_token_score()

    if tokenValidationScore == 0:
        return jsonify({"error": "Invalid token, Please Login again"}), 401
    
    employeeOperation = EmployeeOperations(id)

    if request.method == 'GET':
        employee = employeeOperation.view_emp()
        return jsonify(employee)

    if request.method == 'PUT' and tokenValidationScore > 1:
        data = request.json
        response = employeeOperation.update_emp(data)
        return jsonify(response)
    else:
        return render_template('404.html', message = "You are not allowed to access this functionality.")

    if request.method == 'DELETE' and tokenValidationScore > 2:
        response = employeeOperation.delete_emp()
        return jsonify(response)
    else:
        return render_template('404.html', message = "You are not allowed to access this functionality.")

@app.route('/logout', methods=['POST'])
def logout():
    return redirect('/')

@app.route('/check')
def check():
    token = request.cookies.get('token')
    if token == None:
        return("None")
    else:    
        print(token)
        tokenValidator = TokenValidation(token)
        tokenValidationScore = tokenValidator.get_token_score()
        print(tokenValidationScore)
        return("tokenValidationScore")


if __name__ == '__main__':
    app.run(debug=True)

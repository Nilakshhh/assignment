from flask import Flask, request, jsonify, render_template
from models.employee import Employee
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'encode!it!for!safety'

@app.route('/')
def enter():
    return render_template('login.html')

@app.route('/login', methods = ["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    if not email or not password:
        return 'Missing email or password', 400

    employee = Employee(email, password, role)
    login_status = employee.authenticate(email, password, role)

    if login_status:
        # Create JWT token
        token = jwt.encode({"email": email}, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({'message': 'Invalid email or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
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
        current_time = datetime.datetime.utcnow()

        # Time after 5 minutes
        expiration_time = current_time + datetime.timedelta(minutes=5)
        token = jwt.encode({"email": email, "role": role, "current_time": current_time, "expiration_time": expiration_time}, app.config['SECRET_KEY'], algorithm="HS256")
        response = make_response(redirect(url_for('profile')))

        # Set the token as a cookie in the response
        response.set_cookie('token', token)
        return response

    return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/profile')
def profile():
    token = request.cookies.get('token')
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    print(payload)
    role = payload.get('role')
    return render_template('profile.html', token=token, role=role)

@app.route('/view_emp')
def view_emp():
    token = request.cookies.get('token')
    payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    # Get the current time
    current_time = datetime.datetime.utcnow()

    # Get the expiration time from the payload
    expiration_time = payload['expiration_time']
    role = payload['role']

    # Check if the current time is within the timeframe
    if current_time < expiration_time and role=='employee':
        print("Token is valid and within the timeframe.")
    else:
        print("Token has expired.")


if __name__ == '__main__':
    app.run(debug=True)

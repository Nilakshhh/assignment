
# Role-based User Authentication

This project is aimed at making a role-based user authentication system using Python(Flask), PostgreSQL, HTML+Javascript(frontend). Users are divided into admin, manager and employee with varying permissions depending upon role in the organisation. PyJWT is also applied for jwt based authentication. At login, a jwt token is stored which is used during subsequent requests for authentication. 


## Installation

#### Create a clone of the repository in your local system
```
git clone https://github.com/Nilakshhh/assignment.git
```

Further, the project runs in a virtual python environment where the required packages are installed. Run following commands in your terminal inside project directory

```
python3 -m venv myenv
```
#### To activate the virtual environment
On windows:
```
myenv\Scripts\activate
```
On MacOS and Linux:
```
source myenv/bin/activate
```

Following command will install the required packages:
```
pip install -r requirements.txt
```

Run the system using 
```
python app.py
```

    
## Features

- **User Roles:** The system defines user roles into admin, manager and employees based on permissions and responsibilities assigned to the user

- **Role Based Access Control:** Permissions defined with each role are administered at multiple levels and can be administered by the administrator

- **Administrator management:** Administrator can add, update or delete employees or managers, manager can update or add employees.

- **User-Interface:** A basic User Interface has been made for interaction with api routes and sending requests and recieving response from the server.


## Demo

Insert gif or link to demo


import psycopg2
from config import Config
import json 

db_details = Config.DATABASE_CONFIG

#----------------------------------------------#
    # Class Employee is used to create an employee object and 
    # is responsible for authentication of employee, during login
    # it verifies that mentioned email is present, mentioned role 
    # is correct and also verifies the password
#----------------------------------------------#

class Employee:
    def __init__(self, email, password, role=None, created_at=None):
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
    
    
    def authenticate(self):
        try:
            # connect to PostgreSQL database
            self.conn = psycopg2.connect(
                dbname=db_details['dbname'],
                user=db_details['user'],
                password=db_details['password'],
                host=db_details['host'],
                port=db_details['port']
            )

            self.cur = self.conn.cursor()
            self.cur.execute("SELECT email, password, role FROM employee WHERE email = %s", (self.email,))

            result = self.cur.fetchone()
            
            # If provided email is not present in the database
            if not result:
                response = {'authenticated': False, 'message': 'Email not found in the database'}
            else:
                # Extract stored password and role
                stored_password = result[1]
                self.role = result[2]

                # Check if provided password matches stored password
                if stored_password == self.password:
                    response = {'authenticated': True, 'message': 'Logged in successfully'}
                else:
                    response = {'authenticated': False, 'message': 'Incorrect password'}

            # Close cursor and connection
            self.cur.close()
            self.conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while self.connecting to PostgreSQL:", error)
            response = {'authenticated': False, 'message': 'Problem connecting to database'}

        return json.dumps(response)
import psycopg2
from config import Config
import json 

db_details = Config.DATABASE_CONFIG

class Employee:
    def __init__(self, email, password, role, created_at=None):
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
    
    
    def authenticate(self, email, password, role):
        try:
            # connect to your PostgreSQL database
            self.conn = psycopg2.connect(
                dbname=db_details['dbname'],
                user=db_details['user'],
                password=db_details['password'],
                host=db_details['host'],
                port=db_details['port']
            )

            # Create a cursor object
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT email, password, role FROM employee WHERE email = %s", (email,))

            result = self.cur.fetchone()

            if not result:
                response = {'authenticated': False, 'message': 'Email not found in the database'}
            else:
                # Extract stored password and role
                stored_password = result[1]
                stored_role = result[2]

                # Check if provided role matches stored role
                if role != stored_role:
                    response = {'authenticated': False, 'message': 'Incorrect role'}

                elif stored_password == password:
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
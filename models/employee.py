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

            # Execute a SQL query to fetch user credentials
            self.cur.execute("SELECT email, password, role FROM employee WHERE email = %s", (self.email,))

            # Fetch the result
            result = self.cur.fetchone()
            self.cur.close()
            self.conn.close()

            # Check if user exists and password matches
            if not result:
                response = {'authenticated': False, 'message': 'Email not present in our database'}
            else:
                if result[1] != self.password or result[2] != self.role:
                    response = {'authenticated': False, 'message': 'Incorrect password or role'}
                else:
                    response = {'authenticated': True, 'message': 'Logged in successfully.'}

        except (Exception, psycopg2.Error) as error:
            print("Error while self.connecting to PostgreSQL:", error)
            response = {'authenticated': False, 'message': 'Problem connecting to database'}

        return json.dumps(response)
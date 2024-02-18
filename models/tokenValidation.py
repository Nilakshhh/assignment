import jwt
import datetime
import psycopg2
from config import Config

secret_key = Config.SECRET_KEY
db_details = Config.DATABASE_CONFIG

#----------------------------------------------#
    # Class TokenValidation is used to assign a token 
    # validation score to based on expiration time, 
    # role and email prescence in the database, 
    # 3 is assigned to manager, 2 for manager, 
    # 1 for employee, 0 or -1 for expired token
#----------------------------------------------#

class TokenValidation:
    def __init__(self, token):
        self.token = token
        self.token_score = self.validate()

    def get_token_score(self):
        return self.token_score

    def validate(self):
        if self.token is None:
            return 0
        try:
            payload = jwt.decode(self.token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return 0

        current_time = datetime.datetime.utcnow()
        current_time_str = current_time.isoformat()

        self.email = payload['email']
        self.role = payload['role']
        self.expiration_time = payload['expiration_time']

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
        self.cur.execute("SELECT email, role FROM employee WHERE email = %s", (self.email,))
        
        result = self.cur.fetchone()
        
        self.cur.close()
        self.conn.close()
        
        # Check if user exists and password matches
        if result and result[1] == self.role:
            if self.role == "admin":
                return 3
            elif self.role == "manager" and self.expiration_time > current_time_str:
                return 2
            elif self.role == "employee" and self.expiration_time > current_time_str:
                return 1
            else:
                return 0  # Role expired
        else:
            return -1  # Authentication failed

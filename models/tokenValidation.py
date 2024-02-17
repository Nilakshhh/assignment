import jwt
import datetime
import psycopg2
from config import Config

secret_key = Config.SECRET_KEY

class TokenValidation:
    def __init__(self, token):
        self.token = token
        self.token_score = self.validate(self.token)

    def get_token_score(self):
        return self.token_score

    def validate(self, token):
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return 0

        current_time = datetime.datetime.utcnow()
        current_time_str = current_time.isoformat()

        self.email = payload['email']
        self.role = payload['role']
        self.expiration_time = payload['expiration_time']

        conn = psycopg2.connect(
                dbname="emp",
                user="postgres",
                password="root",
                host="localhost",
                port="5432"
        )

        # Create a cursor object
        cur = conn.cursor()

        # Execute a SQL query to fetch user credentials
        cur.execute("SELECT email, role FROM employee WHERE email = %s", (self.email,))
        
        # Fetch the result
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        # Check if user exists and password matches
        if result and result[1] == self.role:
            pass
        else:
            return -1

        if self.role == "admin":
            return 3
        else:
            if self.expiration_time > current_time_str:
                if self.role == "manager":
                    return 2
                elif self.role == "employee":
                    return 1
            else:
                return 0

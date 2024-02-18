import jwt
import datetime
from config import Config

secret_key = Config.SECRET_KEY

#----------------------------------------------#
    # Class TokenGenerator is used to generate jwt token
    # using employee object as a reference, this token 
    # is stored in cookies and later used for 
    # authentication while requests are made to the server
#----------------------------------------------#
class TokenGenerator:
    def __init__(self, employee):
        self.employee = employee

    def generate_token(self):
        current_time = datetime.datetime.utcnow()
        current_time_str = current_time.isoformat()

        expiration_time = current_time + datetime.timedelta(minutes=600)
        expiration_time_str = expiration_time.isoformat()

        payload = {
            "email": self.employee.email,
            "role": self.employee.role,
            "login_time": current_time_str,
            "expiration_time": expiration_time_str
        }

        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token

import psycopg2

class Employee:
    def __init__(self, email, password, role, created_at=None):
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at
    
    
    def authenticate(self, email, password, role):
        if not self.validate():
            return False
        try:
            # Connect to your PostgreSQL database
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
            cur.execute("SELECT email, password, role FROM employee WHERE email = %s", (self.email,))

            # Fetch the result
            result = cur.fetchone()
            cur.close()
            conn.close()

            # Check if user exists and password matches
            if result and result[1] == self.password and result[2] == self.role:
                return True
            else:
                return False

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)
            return False

    def validate(self):
        return True
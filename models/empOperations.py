import psycopg2
from datetime import date
from psycopg2 import sql

class EmployeeOperations:
    def __init__(self, search_id = 0):
        self.search_id = search_id

    def view_all(self):
        conn = psycopg2.connect(
            dbname="emp",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT id, email, role, created_at FROM employee")
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return employees
    
    def view_emp(self):
        conn = psycopg2.connect(
            dbname="emp",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        cur.execute("SELECT email, role, created_at FROM employee WHERE id = %s", (self.search_id,))
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return employees

    def add_user(self, email, password, role):
        conn = psycopg2.connect(
            dbname="emp",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        try:
            
            cur.execute("SELECT COUNT(*) FROM employee WHERE email = %s", (email,))
            count = self.cur.fetchone()[0]
            if count > 0:
                print("User with this email already exists.")
                return
            
            query = sql.SQL("INSERT INTO employee (email, password, role, created_at) VALUES (%s, %s, %s, %s)")
            
            # Execute the query
            cur.execute(query, (email, password, role, date.today()))
            
            # Commit the transaction
            conn.commit()

            cur.close()
            conn.close()
            
            print("User added successfully.")
        
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting user:", error)
            self.conn.rollback()

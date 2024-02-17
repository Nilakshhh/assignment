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
        cur.execute("SELECT id, email, role, created_at FROM employee WHERE id = %s", (self.search_id,))
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return employees

    def add_user(self, email, password, role):
        self.conn = psycopg2.connect(
            dbname="emp",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()
        try:
            
            self.cur.execute("SELECT COUNT(*) FROM employee WHERE email = %s", (email,))
            count = self.cur.fetchone()[0]
            if count > 0:
                print("User with this email already exists.")
                return
            
            query = sql.SQL("INSERT INTO employee (email, password, role, created_at) VALUES (%s, %s, %s, %s)")
            
            # Execute the query
            self.cur.execute(query, (email, password, role, date.today()))
            
            # Commit the transaction
            self.conn.commit()

            self.cur.close()
            self.conn.close()
            
            print("User added successfully.")
        
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting user:", error)
            self.conn.rollback()

    def update_emp(self, data):
        conn = psycopg2.connect(
            dbname="emp",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        email = data['email']
        role = data['role']
        password = data['password']
        
        try:
            
            sql = """
            UPDATE employee 
            SET email = %s, role = %s, password = %s 
            WHERE id = %s
            """
            # Execute the query
            cur.execute(sql, (email, role, password, self.search_id))
            
            # Commit the transaction
            conn.commit()

            cur.close()
            conn.close()
            
            print("User added successfully.")
            return {"success": True, "message": "User updated successfully"}
        
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting user:", error)
            self.conn.rollback()
            return {"success": False, "error": str(error)}

    def delete_emp(self):
        conn = psycopg2.connect(
            dbname="emp",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )

        try:
            cur = conn.cursor()

            query = "DELETE FROM employee WHERE id = %s;"

            cur.execute(query, (self.search_id,))

            conn.commit()

            cur.close()
            conn.close()

            return {"success": True, "message": f"Employee with ID {self.search_id} deleted successfully."}
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            conn.rollback()

            if conn is not None:
                conn.close()

            return {"success": False, "message": f"Failed to delete employee with ID {self.id}."}

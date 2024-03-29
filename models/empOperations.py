import psycopg2
from datetime import date
from psycopg2 import sql
from config import Config

db_details = Config.DATABASE_CONFIG

#----------------------------------------------#
    # Class EmployeeOperations is responsible for
    # various operations related request handling, 
    # viewing all employees, searching for a single employee
    # adding, updating or deleting a user 
#----------------------------------------------#

class EmployeeOperations:
    def __init__(self, search_id = 0):
        self.search_id = search_id
        self.conn = psycopg2.connect(
            dbname=db_details['dbname'],
            user=db_details['user'],
            password=db_details['password'],
            host=db_details['host'],
            port=db_details['port']
        )

    def view_all(self):
        # Connect to database and retrieve all employee data
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT id, email, role, created_at FROM employee")
        employees = self.cur.fetchall()
        self.cur.close()

        return employees
    
    def view_emp(self):
        # Search for a employee with their id
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT id, email, role, created_at FROM employee WHERE id = %s", (self.search_id,))
        employees = self.cur.fetchall()

        # If no employee are found, return None
        if not employees:
            return None

        self.cur.close()
        
        return employees

    def add_user(self, email, password, role):
        # Connect to database
        self.cur = self.conn.cursor()

        try:
            self.cur.execute("SELECT COUNT(*) FROM employee WHERE email = %s", (email,))
            count = self.cur.fetchone()[0]
            
            # Return 409 if email is already present in database
            if count > 0:
                self.cur.close()
                return "User with this email already exists ", 409

            query = sql.SQL("INSERT INTO employee (email, password, role, created_at) VALUES (%s, %s, %s, %s)")
            self.cur.execute(query, (email, password, role, date.today()))
            
            self.conn.commit()
            self.cur.close()
            
            # Return 200 Success if done
            return "User added successfully.", 200 
        
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting user:", error)
            self.conn.rollback()
            return "Error while inserting user: " + str(error), 500  # 500: Internal Server Error

    def update_emp(self, data):

        self.cur = self.conn.cursor()
        email = data['email']
        role = data['role']
        password = data['password']
        
        try:
            
            sql = """
            UPDATE employee 
            SET email = %s, role = %s, password = %s 
            WHERE id = %s
            """

            self.cur.execute(sql, (email, role, password, self.search_id))
            
            self.conn.commit()
            self.cur.close()
            
            # Return success message if user updated
            return {"success": True, "message": "User updated successfully"}
        
        except (Exception, psycopg2.Error) as error:
            print("Error while inserting user:", error)
            self.conn.rollback()
            return {"success": False, "error": str(error)}

    def delete_emp(self):
        try:
            self.cur = self.conn.cursor()

            query = "DELETE FROM employee WHERE id = %s;"

            self.cur.execute(query, (self.search_id,))

            self.conn.commit()

            self.cur.close()

            return {"success": True, "message": f"Employee with ID {self.search_id} deleted successfully."}
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            self.conn.rollback()

            if self.conn is not None:
                self.conn.close()

            return {"success": False, "message": f"Failed to delete employee with ID {self.id}."}

    def __del__(self):
        if self.conn:
            self.conn.close()
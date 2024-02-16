import psycopg2

class EmployeeOperations:
    def __init__(self, search_id = 0):
        self.search_id = search_id
        if self.search_id==0:
            self.view_all()
        else:
            self.view_emp(self.search_id)

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
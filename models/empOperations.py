import psycopg2

class EmployeeOperations:
    def __init__(self, search_id):
        self.search_id = search_id
        if self.search_id==0:
            self.view_all()
        else:
            self.view_emp(self.search_id)

    def view_all(self):
        pass

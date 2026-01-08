
import json
import os
import datetime

class EmployeeManager:
    def __init__(self, db_file="employees.json"):
        self.db_file = db_file
        self.employees = {}
        self.load_db()

    def load_db(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    self.employees = json.load(f)
            except:
                self.employees = {}
        else:
            self.employees = {}

    def save_db(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.employees, f, indent=4)

    def add_employee(self, name, emp_id, role, dept):
        self.employees[name] = {
            "id": emp_id,
            "role": role,
            "dept": dept,
            "joined": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Active"
        }
        self.save_db()

    def get_employee(self, name):
        return self.employees.get(name, {})

    def delete_employee(self, name):
        if name in self.employees:
            del self.employees[name]
            self.save_db()

    def get_all_employees(self):
        return self.employees

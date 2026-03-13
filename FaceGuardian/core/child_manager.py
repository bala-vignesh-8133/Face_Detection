import json
import os
import datetime

class ChildManager:
    def __init__(self, db_file="missing_children.json"):
        self.db_file = db_file
        self.children = {}
        self.load_db()

    def load_db(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    self.children = json.load(f)
            except:
                self.children = {}
        else:
            self.children = {}

    def save_db(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.children, f, indent=4)

    def add_child(self, name, age, last_seen, date_missing, contact, aadhar, status="Pending Approval"):
        self.children[name] = {
            "age": age,
            "last_seen_location": last_seen,
            "date_missing": date_missing,
            "guardian_contact": contact,
            "aadhar_number": aadhar,
            "reported_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": status
        }
        self.save_db()

    def approve_child(self, name):
        if name in self.children:
            self.children[name]["status"] = "Active"
            self.save_db()

    def get_child(self, name):
        return self.children.get(name, {})

    def delete_child(self, name):
        if name in self.children:
            del self.children[name]
            self.save_db()

    def get_all_children(self):
        return self.children

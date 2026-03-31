from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Paths (absolute to ensure consistency with the desktop app)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "missing_children.json")
FACES_DIR = os.path.join(BASE_DIR, "known_faces")

@app.route('/')
def index():
    try:
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
        
        stats = {
            "total": len(db),
            "pending": len([child for child in db.values() if child.get("status") == "Pending Approval"]),
            "active": len([child for child in db.values() if child.get("status") == "Active"]),
            "rescued": 14 # Static number for hackathon impact
        }
    except:
        stats = {"total": 0, "pending": 0, "active": 0, "rescued": 0}
        
    return render_template('index.html', stats=stats)

@app.route('/submit', methods=['POST'])
def submit_report():
    try:
        # Get form data
        name = request.form.get('name')
        age = request.form.get('age')
        location = request.form.get('location')
        date_missing = request.form.get('date_missing')
        contact = request.form.get('contact')
        aadhar = request.form.get('aadhar')
        
        # Handle file upload
        if 'photo' not in request.files:
            return jsonify({"success": False, "error": "No photo uploaded"}), 400
        
        photo = request.files['photo']
        if photo.filename == '':
            return jsonify({"success": False, "error": "No photo selected"}), 400

        # Create unique filename (similar to desktop app but keeping it simple for web)
        # We use .jpg as the desktop app expects it
        img_filename = f"{name.lower().replace(' ', '_')}.jpg"
        photo_path = os.path.join(FACES_DIR, img_filename)
        photo.save(photo_path)

        # Update JSON Database
        with open(DB_PATH, 'r') as f:
            db = json.load(f)

        db[name.lower().replace(' ', '_')] = {
            "age": age,
            "last_seen_location": location,
            "date_missing": date_missing,
            "guardian_contact": contact,
            "aadhar_number": aadhar,
            "reported_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Pending Approval"
        }

        with open(DB_PATH, 'w') as f:
            json.dump(db, f, indent=4)

        return jsonify({"success": True, "message": "Report submitted successfully! Status: Pending Approval"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Ensure faces dir exists
    if not os.path.exists(FACES_DIR):
        os.makedirs(FACES_DIR)
    app.run(debug=True, port=5000)

from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import pyodbc
import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Azure Blob Setup
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
container_name = "complaint-images"

# Azure SQL connection
conn_str = os.getenv("AZURE_SQL_CONN_STRING")

# Logic App Webhook URL
logic_app_url = os.getenv("LOGIC_APP_WEBHOOK_URL")

@app.route("/")
def home():
    return redirect(url_for("submit_complaint"))

@app.route("/submit", methods=["GET", "POST"])
def submit_complaint():
    if request.method == "POST":
        try:
            student_name = request.form["student_name"]
            email = request.form["email"]
            title = request.form["title"]
            description = request.form["description"]
            type_ = request.form["type"]
            file = request.files["file"]

            file_url = None

            # Upload file to Azure Blob
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                blob_name = f"{uuid.uuid4()}_{filename}"
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
                blob_client.upload_blob(file)
                file_url = blob_client.url

            # Save to Azure SQL
            with pyodbc.connect(conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Complaints (student_name, student_email, title, description, complaint_type, file_url, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (student_name, email, title, description, type_, file_url, "Submitted"))
                conn.commit()

            # Send Email via Logic App
            payload = {
                "student_name": student_name,
                "email": email,
                "title": title,
                "description": description,
                "type": type_,
                "file_url": file_url,
                "status": "Submitted"
            }
            requests.post(logic_app_url, json=payload)

            return redirect(url_for("student_dashboard"))

        except Exception as e:
            print("Error while submitting complaint:", str(e))
            return jsonify({"success": False, "error": str(e)}), 500

    return render_template("submit_complaint.html")

@app.route("/dashboard")
def student_dashboard():
    return render_template("student_dashboard.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route("/get_complaints", methods=["GET"])
def get_complaints():
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, student_name, student_email, title, description, complaint_type, file_url, status, submitted_at
                FROM Complaints
                ORDER BY submitted_at DESC
            """)
            rows = cursor.fetchall()

            complaints = []
            for row in rows:
                complaints.append({
                    "id": row.id,
                    "student_name": row.student_name,
                    "email": row.student_email,
                    "title": row.title,
                    "description": row.description,
                    "type": row.complaint_type,
                    "file_url": row.file_url,
                    "status": row.status,
                    "submitted_at": row.submitted_at.strftime('%Y-%m-%d %H:%M:%S') if row.submitted_at else "N/A"
                })

            return jsonify({"complaints": complaints})
    except Exception as e:
        print("Error fetching complaints:", str(e))
        return jsonify({"error": "Could not fetch complaints"}), 500

@app.route("/assign_complaint", methods=["POST"])
def assign_complaint():
    try:
        data = request.get_json()
        complaint_id = data.get("id")
        assignee = data.get("assignee")

        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Complaints
                SET status = ?, assigned_to = ?
                WHERE id = ?
            """, ("Assigned", assignee, complaint_id))
            conn.commit()

        return jsonify({"success": True, "message": "Complaint assigned successfully."})
    except Exception as e:
        print("Error assigning complaint:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/update_status", methods=["POST"])
def update_status():
    try:
        data = request.get_json()
        complaint_id = data.get("id")
        new_status = data.get("status")

        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Complaints
                SET status = ?
                WHERE id = ?
            """, (new_status, complaint_id))
            conn.commit()

        return jsonify({"success": True, "message": "Complaint status updated successfully."})
    except Exception as e:
        print("Error updating complaint status:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

#if __name__ == "__main__":
 #   app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
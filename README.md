# 📢 Complaint Management System

A web-based application designed to streamline the submission, tracking, and resolution of user complaints. Built using Python and deployed on Microsoft Azure, this system is ideal for institutions or organizations aiming to improve transparency and accountability.

## 🛠️ Features

- 🔐 User-friendly complaint submission form
- 📄 Attachments support (PDF, images, etc.)
- 🗃️ Complaint categorization (e.g., Technical, Academic, Facility)
- 📬 Admin dashboard for tracking and updating statuses
- 📊 Sort and filter complaints by date, type, status
- 📨 Email notification system (optional)

---

## 🧑‍💻 Tech Stack

| Frontend        | Backend         | Database      | Deployment      |
|----------------|------------------|---------------|-----------------|
| HTML, CSS, JS   | Python (Flask/Django) | SQL Server / MySQL | Azure App Service |

---

## 🚀 Getting Started (Local Setup)

```bash
# 1. Clone the repo
git clone https://github.com/Rorychhattish/Voicepoint--Student-Complaint-Management-System.git
cd Voicepoint--Student-Complaint-Management-System

# 2. Create virtual environment & activate
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py              # or: flask run / python manage.py runserver
🔧 Environment Variables
Create a .env file or configure in Azure:

env

DB_HOST=your-database-host
DB_NAME=your-db-name
DB_USER=your-db-username
DB_PASSWORD=your-db-password
SECRET_KEY=your-secret-key
PORT=8000
☁️ Deployment (Azure App Service)

Link Azure App Service to the GitHub repo (via Deployment Center)

Set environment variables in Azure → Configuration

Make sure to include requirements.txt and the proper startup command

Monitor logs in Azure using Log Stream


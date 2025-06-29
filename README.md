# Doctor Appointment System

A full-stack web application that enables patients to book appointments with doctors and allows doctors/admins to manage schedules and records. It is built with **Python Flask** for the backend and **HTML/CSS with Bootstrap** for the frontend.

## Features

- User authentication for patients and doctors
- Book and manage appointments
- Role-based access control (Admin / Doctor / Patient)
- Admin dashboard for managing users and appointments
- Responsive frontend using Bootstrap
- Templating with Flask and Jinja2

## Tech Stack

| Layer     | Technology         |
|-----------|--------------------|
| Frontend  | HTML, CSS, Bootstrap |
| Backend   | Python Flask       |
| Templating | Jinja2            |
| Database  | SQLite / MySQL     |



## Clone the repository

git clone https://github.com/Anuprema/doctor--appointment-system.git
cd doctor--appointment-system

## Set up virtual environment

python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Or on Mac/Linux
source venv/bin/activate

## Install dependencies

pip install -r requirements.txt

## Run the application
python app.py
Then open your browser and go to: http://127.0.0.1:5000

 ## Folder Structure
doctor--appointment-system/
├── static/             # CSS, Bootstrap, assets
├── templates/          # HTML pages (Jinja2 templates)
├── app.py              # Main Flask app
├── requirements.txt    # Python dependencies
└── README.md           # This file

Author
Anuprema A


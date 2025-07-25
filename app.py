from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "doctor" or "patient"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/images')
def images():
    return render_template('images.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        role = request.form['role']

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Choose a different one.", "danger")
            return redirect(url_for('register'))

        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('appointment'))
        flash("Invalid username or password.", "danger")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # If using Flask-Login
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    if request.method == 'POST':
        doctor_name = request.form['doctor_name']
        doctor = User.query.filter_by(username=doctor_name, role="doctor").first()

        if not doctor:
            flash("Doctor does not exist. Please enter a valid doctor's username.", "danger")
            return redirect(url_for('appointment'))

        new_appointment = Appointment(
            patient_name=current_user.username,
            doctor_name=doctor.username,
            date=request.form['date'],
            time=request.form['time'],
            user_id=current_user.id
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash("Appointment booked successfully!", "success")
        return redirect(url_for('view_appointments'))

    doctors = User.query.filter_by(role="doctor").all()
    return render_template('appointment.html', doctors=doctors)

@app.route('/view_appointments')
@login_required
def view_appointments():
    if current_user.role == "doctor":
        appointments = Appointment.query.filter_by(doctor_name=current_user.username).all()
    else:
        appointments = Appointment.query.filter_by(user_id=current_user.id).all()

    return render_template('view_appointments.html', appointments=appointments)

@app.route('/edit_appointment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)

    if current_user.role != "patient" or appointment.user_id != current_user.id:
        flash("You are not authorized to edit this appointment.", "danger")
        return redirect(url_for('view_appointments'))

    if request.method == 'POST':
        appointment.date = request.form['date']
        appointment.time = request.form['time']
        db.session.commit()
        flash("Appointment updated successfully!", "success")
        return redirect(url_for('view_appointments'))

    return render_template('edit_appointment.html', appointment=appointment)

@app.route('/delete_appointment/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)

    if current_user.role != "patient" or appointment.user_id != current_user.id:
        flash("You are not authorized to delete this appointment.", "danger")
        return redirect(url_for('view_appointments'))

    db.session.delete(appointment)
    db.session.commit()
    flash("Appointment deleted successfully!", "danger")
    return redirect(url_for('view_appointments'))

def add_default_doctors():
    doctors = ["Dr. John Smith", "Dr. Sarah Lee", "Dr. Michael Brown", "Dr. Emily Davis"]
    for doctor_name in doctors:
        existing_doctor = User.query.filter_by(username=doctor_name, role="doctor").first()
        if not existing_doctor:
            hashed_password = bcrypt.generate_password_hash("doctor123").decode('utf-8')
            new_doctor = User(username=doctor_name, password=hashed_password, role="doctor")
            db.session.add(new_doctor)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        add_default_doctors()
    app.run(debug=True)

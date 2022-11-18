from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from constants import SECRET_KEY, DB_URL
from utils import register_user, login_user, predict, get_nutrition_value, save_image
from datetime import datetime

app = Flask(__name__)

# CONFIG
app.config["SECRET_KEY"] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

class User(UserMixin, db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(15), nullable=False)
   email = db.Column(db.String(50), unique=True, nullable=False)
   password = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/')
@login_required
def home_route():
    if not current_user.is_authenticated:
        return redirect("/login")

    email = current_user.email
    return render_template('index.html', email=email)

@app.route('/register', methods=['GET','POST'])
def register_route():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        register_user(db, User, username, email, password)

        return redirect('/')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST']) 
def login_route():
    if request.method == "POST":
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        login_success = login_user(User, email, password)

        if not login_success:
            return redirect('/login')
            
        return redirect('/')

    return render_template('login.html')


@app.route('/api/predict', methods=["POST"])
@login_required
def predict_route():
    if request.method != "POST":
        return render_template('index.html')

    file = request.files["file"]
    file_path = save_image(file)
    prediction = predict(file_path)

    nutrition = get_nutrition_value(prediction)

    return {"label": prediction, 'nutrition': nutrition}

"""
SQL QUERY TO CREATE TABLE:

CREATE TABLE user(
    id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
"""
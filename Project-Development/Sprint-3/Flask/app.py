from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from constants import SECRET_KEY, DB_URL
from utils import register_user, login_user, predict, get_nutrition_value, save_image, auth_middleware
from datetime import datetime

app = Flask(__name__)

# CONFIG
app.config["SECRET_KEY"] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(50), unique=True, nullable=False)
   password = db.Column(db.String(50), nullable=False)

@app.route('/')
def home_route():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register_route():
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        register_user(db, User, email, password)

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
@auth_middleware(User)
def predict_route():
    if request.method != "POST":
        return render_template('index.html')

    file = request.files["file"]
    file_path = save_image(file)
    prediction = predict(file_path)

    nutrition = get_nutrition_value(prediction)

    return {"label": prediction, 'nutrition': nutrition}

"""
CREATE TABLE user(id VARCHAR(255) PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL);


"""
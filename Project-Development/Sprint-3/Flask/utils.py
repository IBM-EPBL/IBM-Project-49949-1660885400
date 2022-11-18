from flask import request
from werkzeug.security import generate_password_hash,check_password_hash
from keras.preprocessing.image import image_utils
from keras.models import load_model
from requests import get
from os import path
from functools import wraps
import numpy as np
import uuid
import datetime
import jwt

from constants import API_HEADERS, API_URL, SECRET_KEY

model = load_model('./model.h5')
print("\nModel loaded\n")

def save_image(file):
    root_path = path.dirname(__file__)
    file_path = path.join(root_path, 'uploads', file.filename)
    file.save(file_path)

    print(f"\nFILE SAVED: {file.filename} at {file_path}\n")
    return file_path

def predict(file_path):
    # preprocessing the image
    file = image_utils.load_img(file_path, target_size=(64,64))
    file = image_utils.img_to_array(file)
    x = np.expand_dims(file, axis=0)

    # classifying the image
    prediction = model.predict(x)[0]
    max_index = np.where(prediction == np.amax(prediction))[0]
    labels = ["Apple", 'Banana', 'Orange', 'Pineapple', 'Watermelon']

    print(f"""
PREDICTIONS: 
 - {labels[0]} = {prediction[0]}
 - {labels[1]} = {prediction[1]}
 - {labels[2]} = {prediction[2]}
 - {labels[3]} = {prediction[3]}
 - {labels[4]} = {prediction[4]}
    """)

    predicted_label = labels[max_index[0]]

    print(f"PREDICTION RESULT: {predicted_label}\n")
    return predicted_label

def get_nutrition_value(fruit):
    response = get(API_URL, headers=API_HEADERS, params={"query": fruit})
    data = response.json()
    items = data.get('items', [])
    item = items[0] if len(items) > 0 else None

    print(f"\nRESPONSE: {item}\n")
    return item

def auth_middleware(func):
    @wraps
    def decorator(User, *args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {'message': 'Token is missing!'}, 401

        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return {'message': 'Token is invalid!'}, 401

        return func(current_user, *args, **kwargs)
    
    return decorator

def register_user(db, User, email, password):
    hashed_password = generate_password_hash(password, method='sha256')

    user = User(id= str(uuid.uuid4()), email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

def login_user(User, email, password):
    user = User.query.filter_by(email=email).first()
    if check_password_hash(user.password, password):
        return True

    return False
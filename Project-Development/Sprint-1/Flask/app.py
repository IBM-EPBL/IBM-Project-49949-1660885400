from flask import Flask, render_template, request
from os import path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predict', methods=["POST"])
def predict():
    if request.method != "POST":
        return render_template('index.html')

    print(request.files)
    # getting the image and saving it locally
    image = request.files["file"]
    root_path = path.dirname(__file__)
    image_path = path.join(root_path, 'uploads', image.filename)
    image.save(image_path)

    return {"url": image_path}
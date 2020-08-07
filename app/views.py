from app import app
from flask import render_template

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('upload.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/<guid>")
def download(guid):
    return f"<h1>Get file: {guid}</h1>"
# application.py
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/<guid>")
def download(guid):
    return f"<h1>Get file: {guid}</h1>"

if __name__ == "__main__":
    app.run()
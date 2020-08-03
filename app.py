# application.py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello World!</h1>"

@app.route("/<guid>")
def download(guid):
    return f"<h1>Get file: {guid}</h1>"

if __name__ == "__main__":
    app.run()
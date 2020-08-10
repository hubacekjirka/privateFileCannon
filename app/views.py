from app import app
from flask import render_template, request, redirect
import os

#TBD: put into config,py

currentDir = os.path.dirname(os.path.realpath(__file__))
app.config["fileStoragePath"] = os.path.join(currentDir,"fileStorage",)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file.save(os.path.join(app.config["fileStoragePath"], file.filename))
            return redirect(request.url)
    return render_template("upload.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/<guid>")
def download(guid):
    return f"<h1>Get file: {guid}</h1>"
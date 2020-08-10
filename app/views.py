from app import app
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
import os

#TBD: put into config,py

currentDir = os.path.dirname(os.path.realpath(__file__))
app.config["fileStoragePath"] = os.path.join(currentDir,"fileStorage")
app.config["maxFileSize"] = 100 * 1024 * 1024

def allowedImageFilesize(fileSize):
    if int(fileSize) <= app.config["maxFileSize"]:
        return True

    return False

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print(request.cookies)
        if request.files:
            if not allowedImageFilesize(request.cookies.get("fileSize")):
                #TODO: do flash message
                print(f"File exceeded maximum size of {app.config['maxFileSize'] / 1024 / 1024}MB")
                return redirect(request.url)

            file = request.files["file"]

            if file.filename == "":
                #TODO: change to flash message
                print("Image must have a filename")
                return redirect(request.url)

            fileName = secure_filename(file.filename)

            file.save(os.path.join(app.config["fileStoragePath"], fileName))
            return redirect(request.url)
    return render_template("upload.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/<guid>")
def download(guid):
    return f"<h1>Get file: {guid}</h1>"
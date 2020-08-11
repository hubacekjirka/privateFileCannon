from app import app
from flask import render_template, request, redirect, send_from_directory, abort, flash
from werkzeug.utils import secure_filename
import os

#TBD: put into config,py
app.secret_key = "super secret key"
currentDir = os.path.dirname(os.path.realpath(__file__))
app.config["file_storage_path"] = os.path.join(currentDir,"fileStorage")
app.config["max_file_size"] = 100 * 1024 * 1024

def allowed_image_filesize(file_size):
    if int(file_size) <= app.config["max_file_size"]:
        return True

    return False

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print(request.cookies)
        if request.files:
            if not allowed_image_filesize(request.cookies.get("fileSize")):
                #TODO: do flash message
                print(f"File exceeded maximum size of {app.config['max_file_size'] / 1024 / 1024}MB")
                return redirect(request.url)

            file = request.files["file"]

            if file.filename == "":
                #TODO: change to flash message
                print("Image must have a filename")
                return redirect(request.url)

            file_name = secure_filename(file.filename)

            file.save(os.path.join(app.config["file_storage_path"], file_name))
            flash(f"File uploaded. Link to the file: {request.url_root + 'get_file/' + file_name}" , "info")
            flash(f"To delete the file: {request.url_root + 'remove_file/' + file_name}" , "info")
            return redirect(request.url_root)

    return render_template("upload.html")

@app.route("/about")
def about():
    return render_template("about.html")

#TODO:
#@app.route("/<uuid:guid>")
#def download(guid):
#    return f"<h1>Get file: {guid}</h1>"

@app.route("/get_file/<string:file_name>")
def get_file(file_name):
    print(file_name)

    try:
        return send_from_directory(app.config["file_storage_path"], filename=file_name, as_attachment = True)
    except FileNotFoundError:
        abort(404)

    return(file_name)

@app.route("/remove_file/<string:file_name>")
def remove_file(file_name):
    try:
        os.remove(os.path.join(app.config["file_storage_path"], file_name))
        return(f"{file_name} removed")
    except FileNotFoundError:
        abort(404)
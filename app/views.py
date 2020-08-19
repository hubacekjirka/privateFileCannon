from app import app
from flask import render_template, request, redirect, send_from_directory, abort, flash
from werkzeug.utils import secure_filename
import os

def allowed_image_filesize(file_size):
    if int(file_size) <= app.config["MAX_FILE_SIZE"]:
        return True

    return False

@app.route("/", methods=["GET", "POST"])
def home():
    print(app.config)
    if request.method == "POST":

        # Check if there's any file coming through the form
        if not request.files["file"].filename == "":
            
            # Check file size against app settings, abort storing the file if the max size is exceeded
            if not allowed_image_filesize(request.cookies.get("fileSize")):
                flash(f"File exceeded maximum size of {app.config['MAX_FILE_SIZE'] / 1024 / 1024:.0f} MB", "error")
                return redirect(request.url)

            file = request.files["file"]
            file_name = secure_filename(file.filename)

            file.save(os.path.join(app.config["FILE_STORAGE_PATH"], file_name))
            flash(f"File uploaded. Link to the file: {request.url_root + 'get_file/' + file_name}" , "info")
            flash(f"To delete the file: {request.url_root + 'remove_file/' + file_name}" , "info")
            return redirect(request.url_root)

        # No file submitted by user
        else:
            flash(f"No ammunition provided, sorry ...", "error")
            return redirect(request.url)

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
        return send_from_directory(app.config["FILE_STORAGE_PATH"], filename=file_name, as_attachment = True)
    except FileNotFoundError:
        abort(404)

    return(file_name)

@app.route("/remove_file/<string:file_name>")
def remove_file(file_name):
    try:
        os.remove(os.path.join(app.config["FILE_STORAGE_PATH"], file_name))
        return(f"{file_name} removed")
    except FileNotFoundError:
        abort(404)
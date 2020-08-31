from app import app
from flask import (
    render_template,
    request,
    redirect,
    send_from_directory,
    abort,
    flash,
    jsonify,
    make_response
)
from werkzeug.utils import secure_filename
import os


# Catch 413 error raised when the uploaded file exceeds limit defined in the
# environment variable
@app.errorhandler(413)
def file_size_exceeded(e):
    res = make_response(
        jsonify(
            {
                "message": "The file has exceeded maximum allowed size",
            }
        ),
        413,
    )
    return res


@app.route("/", methods=["GET", "POST"])
def home():
    print(app.config)
    if request.method == "POST":

        if not request.form["upload_password"] == app.config["UPLOAD_PASSWORD"]:
            res = make_response(
                jsonify(
                    {
                        "message": "Invalid password",
                    }
                ),
                403,
            )
            return res

        # Check if there's any file coming through the form
        if not request.files["file"].filename == "":

            file = request.files["file"]
            file_name = secure_filename(file.filename)
            file.save(os.path.join(app.config["FILE_STORAGE_PATH"], file_name))

            # Reokace http with https as the app runs behind proxy
            url_root = request.url_root
            if app.config["HTTPS_PROXY"]:
                url_root = url_root.replace("http", "https")

            res = make_response(
                jsonify(
                    {
                        "message": f"{file_name} uploaded",
                        "get_link": f"{url_root + 'get_file/' + file_name}",
                        "remove_link": f"{url_root + 'remove_file/'}"
                        + f"{file_name}",
                    }
                ),
                200,
            )
            return res

        # No file submitted by user - shouldn't happen, safety net on backend
        else:
            flash("No ammunition provided, sorry ...", "error")
            return redirect(request.url)

    return render_template("upload.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/get_file/<string:file_name>")
def get_file(file_name):
    print(file_name)

    try:
        return send_from_directory(
            app.config["FILE_STORAGE_PATH"], filename=file_name, as_attachment=True
        )
    except FileNotFoundError:
        abort(404)

    return file_name


@app.route("/remove_file/<string:file_name>")
def remove_file(file_name):
    try:
        os.remove(os.path.join(app.config["FILE_STORAGE_PATH"], file_name))
        return f"{file_name} removed"
    except FileNotFoundError:
        abort(404)

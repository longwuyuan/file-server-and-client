# app.py
# File-Ops over REST API
# This code runs a flask server
# The flask server provides APIs to upload, delete & list files, besides a healthcheck API

# Import dependencies
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, request
import os
import time
import humanize

# PATH  of directory to save uploaded files
# This path is created on the host manually.
# Dockerfile consuming this will create this directory
PATH_STORAGE = "./uploads/"


# TODO
# - No current restricted on allowed extensions of files being uploaded.  So do that if/when needed.
# - No spec on securing filenames like .bashrc/.profile for security. So do that if/when needed.
# - Need to research that for the route decorateor, pyright is complaining like below:
#   - Type "() -> (Literal'ok' | None)" is not assignable to type "(...) -> AwaitableResponseReturnValue
#   - __ No overloads for "join" match the provided arguments

app = Flask(__name__)
app.config["PATH_STORAGE"] = PATH_STORAGE
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


# Healthcheck API
@app.route("/healthcheck")
def healthcheck():
    if os.path.exists(PATH_STORAGE):
        return "ok"


# Upload API
@app.route("/upload", methods=["POST"])
def upload():
    # Return if request did not contain file
    if request.method == "POST":
        if "file" not in request.files:
            return "Error: file not provided"
        else:
            file = request.files["file"]
            file_path = os.path.join(app.config["PATH_STORAGE"], file.filename)
            # Avoid overwriting existing file
            if os.path.exists(file_path):
                return "Error: File '%s' exists on the server" % file.filename
            else:
                file.save(file_path)
                return "'%s' uploaded!" % file.filename


# Delete API
@app.route("/delete/<filename>", methods=["DELETE"])
def delete(filename):
    # Return if request did not contain filename
    if request.method == "DELETE":
        if filename == "":
            return "Error: filename not provided"
        else:
            file_path = os.path.join(app.config["PATH_STORAGE"], filename)
            # Avoid overwriting existing file
            if os.path.exists(file_path):
                os.remove(file_path)
                return "File %s deleted." % filename
            else:
                return "Error: file %s does not exist on server" % filename


# List API
@app.route("/list", methods=["GET"])
def list():
    file_list = []
    filestore = os.listdir(PATH_STORAGE)
    for file in filestore:
        filepath = PATH_STORAGE + file
        filesize = humanize.naturalsize(os.path.getsize(filepath))
        filedate_unix = os.path.getmtime(filepath)
        filedate = time.ctime(filedate_unix)
        fileinfo = {"name": file, "size": filesize, "date": filedate}
        file_list.append(fileinfo)
    return file_list

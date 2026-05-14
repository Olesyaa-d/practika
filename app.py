from flask import (
    Flask,
    render_template,
    request
)

import os

from scanner.file_scanner import FileScanner


app = Flask(__name__)

scanner = FileScanner()

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan_file():

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":

        return "Файл не выбран"

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        uploaded_file.filename
    )

    uploaded_file.save(file_path)

    result = scanner.scan_file(file_path)

    return render_template(
        "result.html",
        result=result,
        filename=uploaded_file.filename
    )


if __name__ == "__main__":

    app.run(debug=True)
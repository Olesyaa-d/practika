import os

from flask import Flask, render_template, request

from scanner.pipeline.scanner_pipeline import ScannerPipeline
from scanner.services.file_scanner import FileScanner


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


pipeline = ScannerPipeline()
scanner = FileScanner(pipeline)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan_file():

    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        return "Файл не выбран"

    # путь сохранения файла
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        uploaded_file.filename
    )

    # сохраняем файл
    uploaded_file.save(file_path)

    # запускаем анализ через pipeline
    results = scanner.scan_file(file_path)

    return render_template(
        "result.html",
        results=results,
        filename=uploaded_file.filename
    )


if __name__ == "__main__":
    app.run(debug=True)
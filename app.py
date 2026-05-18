import os

from flask import Flask, render_template, request

from flask_migrate import Migrate

from models import db, Document, ScanResult

from scanner.pipeline.scanner_pipeline import ScannerPipeline
from scanner.services.file_scanner import FileScanner


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# DB (SQLite)
import os as _os

basedir = _os.path.abspath(_os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + _os.path.join(basedir, "database", "app.db")
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
migrate = Migrate(app, db)


pipeline = ScannerPipeline()

from scanner.scanners.email_scanner import EmailScanner
from scanner.scanners.card_scanner import CardScanner
from scanner.scanners.keyword_scanner import KeywordScanner

pipeline.add_scanner(EmailScanner())
pipeline.add_scanner(CardScanner())
pipeline.add_scanner(KeywordScanner())

scanner = FileScanner(pipeline)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan_file():

    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        return "Файл не выбран"

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        uploaded_file.filename
    )

    uploaded_file.save(file_path)

    # читаем файл
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        file_text = f.read()


    # сохраняем документ
    document = Document(
        text=file_text,
        type=uploaded_file.filename.split(".")[-1]
    )

    db.session.add(document)
    db.session.commit()

    # запускаем pipeline (ВАЖНО: теперь это список объектов)
    results = scanner.scan_file(file_path)

    emails = []
    cards = []
    keywords = []

    for r in results:

        # email result
        if hasattr(r, "emails"):
            emails.extend(getattr(r, "emails", []))

        # card result
        if hasattr(r, "cards"):
            cards.extend(getattr(r, "cards", []))

        # keyword result
        if hasattr(r, "keywords"):
            keywords.extend(getattr(r, "keywords", []))


    scan_result = ScanResult(
        document_id=document.id,
        emails=",".join(emails),
        cards=",".join(cards),
        keywords=",".join(keywords)
    )

    db.session.add(scan_result)
    db.session.commit()

    return render_template(
        "result.html",
        emails=emails,
        cards=cards,
        keywords=keywords,
        filename=uploaded_file.filename
    )


if __name__ == "__main__":
    app.run(debug=True)
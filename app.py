import os

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    url_for
)

from models import db, Document, ScanResult

from scanner.pipeline.scanner_pipeline import ScannerPipeline
from scanner.services.file_scanner import FileScanner

from scanner.scanners.email_scanner import EmailScanner
from scanner.scanners.card_scanner import CardScanner
from scanner.scanners.keyword_scanner import KeywordScanner

app = Flask(__name__)


UPLOAD_FOLDER = "uploads"
PROTECTED_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, "protected")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROTECTED_UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(basedir, "database", "app.db")
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


pipeline = ScannerPipeline()

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

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:
        file_text = file.read()

    document = Document(
        text=file_text,
        type="scan",
        filename=uploaded_file.filename,
        file_path=file_path
    )

    db.session.add(document)
    db.session.commit()

    results = scanner.scan_file(file_path)

    emails = []
    cards = []
    keywords = []

    for result in results:

        if hasattr(result, "emails"):
            emails.extend(result.emails)

        if hasattr(result, "cards"):
            cards.extend(result.cards)

        if hasattr(result, "keywords"):
            keywords.extend(result.keywords)

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


@app.route("/protected")
def protected_documents():

    documents = Document.query.filter_by(
        type="защита"
    ).order_by(
        Document.created_at.desc()
    ).all()

    return render_template(
        "protected_documents.html",
        documents=documents
    )


@app.route("/protected/upload", methods=["GET", "POST"])
def upload_protected_document():

    if request.method == "GET":
        return render_template("upload_protected_document.html")

    uploaded_file = request.files.get("file")

    if not uploaded_file or uploaded_file.filename == "":
        return "Файл не выбран"

    file_path = os.path.join(
        PROTECTED_UPLOAD_FOLDER,
        uploaded_file.filename
    )

    uploaded_file.save(file_path)

    with open(
        file_path,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:
        file_text = file.read()

    document = Document(
        text=file_text,
        type="защита",
        filename=uploaded_file.filename,
        file_path=file_path
    )

    db.session.add(document)
    db.session.commit()

    return redirect(url_for("protected_documents"))


@app.route("/protected/<document_id>/download")
def download_protected_document(document_id):

    document = Document.query.get_or_404(document_id)

    if document.type != "защита":
        return "Документ не является защищаемым"

    return send_file(
        document.file_path,
        as_attachment=True,
        download_name=document.filename
    )


@app.route("/protected/<document_id>/delete", methods=["POST"])
def delete_protected_document(document_id):

    document = Document.query.get_or_404(document_id)

    if document.type != "защита":
        return "Документ не является защищаемым"

    if document.file_path and os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.session.delete(document)
    db.session.commit()

    return redirect(url_for("protected_documents"))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
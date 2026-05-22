import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file
)

from models import db, Document, ScanResult

from classifier.naive_bayes_classifier import (
    NaiveBayesClassifier
)

from scanner.pipeline.scanner_pipeline import (
    ScannerPipeline
)

from scanner.services.file_scanner import (
    FileScanner
)

from scanner.scanners.email_scanner import (
    EmailScanner
)

from scanner.scanners.card_scanner import (
    CardScanner
)

from scanner.scanners.keyword_scanner import (
    KeywordScanner
)


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"

PROTECTED_UPLOAD_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "protected"
)

REGULAR_UPLOAD_FOLDER = os.path.join(
    UPLOAD_FOLDER,
    "regular"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    PROTECTED_UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    REGULAR_UPLOAD_FOLDER,
    exist_ok=True
)


basedir = os.path.abspath(
    os.path.dirname(__file__)
)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = (
        "sqlite:///"
        +
        os.path.join(
            basedir,
            "database",
            "app.db"
        )
)

app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False

db.init_app(app)


pipeline = ScannerPipeline()

pipeline.add_scanner(
    EmailScanner()
)

pipeline.add_scanner(
    CardScanner()
)

pipeline.add_scanner(
    KeywordScanner()
)

scanner = FileScanner(
    pipeline
)


@app.route("/")
def index():

    return render_template(
        "index.html"
    )


@app.route(
    "/scan",
    methods=["POST"]
)
def scan_file():

    uploaded_file = request.files.get(
        "file"
    )

    if (
            not uploaded_file
            or
            uploaded_file.filename == ""
    ):
        return "Файл не выбран"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.filename
    )

    uploaded_file.save(
        file_path
    )

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

    db.session.add(
        document
    )

    db.session.commit()


    results = scanner.scan_file(
        file_path
    )

    emails = []
    cards = []
    keywords = []

    for result in results:

        if hasattr(
                result,
                "emails"
        ):
            emails.extend(
                result.emails
            )

        if hasattr(
                result,
                "cards"
        ):
            cards.extend(
                result.cards
            )

        if hasattr(
                result,
                "keywords"
        ):
            keywords.extend(
                result.keywords
            )


    scan_result = ScanResult(

        document_id=document.id,

        emails=",".join(
            emails
        ),

        cards=",".join(
            cards
        ),

        keywords=",".join(
            keywords
        )
    )

    db.session.add(
        scan_result
    )

    db.session.commit()


    classification = None

    protection_reasons = []


    if emails:
        protection_reasons.append(
            "найдены email"
        )

    if cards:
        protection_reasons.append(
            "найдены номера карт"
        )

    if keywords:
        protection_reasons.append(
            "найдены ключевые слова"
        )


    if protection_reasons:

        classification = {

            "predicted_type":
                "защита",

            "method":
                "rules",

            "probabilities": {

                "защита": 1.0,

                "обычный": 0.0
            },

            "reasons":
                protection_reasons
        }

    else:

        # ------------------
        # BAYES
        # ------------------

        training_documents = (
            Document.query.filter(
                Document.type.in_(
                    [
                        "защита",
                        "обычный"
                    ]
                )
            ).all()
        )

        available_types = {

            document.type

            for document

            in training_documents
        }

        if (
                "защита"
                in available_types

                and

                "обычный"
                in available_types
        ):

            classifier = (
                NaiveBayesClassifier()
            )

            classifier.train(
                training_documents
            )

            classification = (
                classifier.predict(
                    file_text
                )
            )

            classification[
                "method"
            ] = "bayes"

            classification[
                "reasons"
            ] = [

                "чувствительные данные не найдены",

                "использован байесовский классификатор"
            ]


    return render_template(

        "result.html",

        filename=uploaded_file.filename,

        emails=emails,

        cards=cards,

        keywords=keywords,

        classification=classification
    )


@app.route("/protected")
def protected_documents():

    documents = Document.query.filter_by(
        type="защита"
    ).all()

    return render_template(
        "protected_documents.html",
        documents=documents
    )


@app.route(
    "/protected/upload",
    methods=["GET", "POST"]
)
def upload_protected_document():

    if request.method == "GET":

        return render_template(
            "upload_protected_document.html"
        )

    uploaded_file = request.files["file"]

    path = os.path.join(
        PROTECTED_UPLOAD_FOLDER,
        uploaded_file.filename
    )

    uploaded_file.save(
        path
    )

    with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
    ) as file:

        text = file.read()

    document = Document(

        text=text,

        type="защита",

        filename=uploaded_file.filename,

        file_path=path
    )

    db.session.add(
        document
    )

    db.session.commit()

    return redirect(
        url_for(
            "protected_documents"
        )
    )


@app.route(
    "/protected/<id>/delete",
    methods=["POST"]
)
def delete_protected_document(id):

    document = (
        Document.query.get_or_404(id)
    )

    db.session.delete(
        document
    )

    db.session.commit()

    return redirect(
        url_for(
            "protected_documents"
        )
    )


@app.route("/regular")
def regular_documents():

    documents = Document.query.filter_by(
        type="обычный"
    ).all()

    return render_template(
        "regular_documents.html",
        documents=documents
    )


@app.route(
    "/regular/upload",
    methods=["GET", "POST"]
)
def upload_regular_document():

    if request.method == "GET":

        return render_template(
            "upload_regular_document.html"
        )

    uploaded_file = request.files["file"]

    path = os.path.join(
        REGULAR_UPLOAD_FOLDER,
        uploaded_file.filename
    )

    uploaded_file.save(
        path
    )

    with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
    ) as file:

        text = file.read()

    document = Document(

        text=text,

        type="обычный",

        filename=uploaded_file.filename,

        file_path=path
    )

    db.session.add(
        document
    )

    db.session.commit()

    return redirect(
        url_for(
            "regular_documents"
        )
    )


@app.route(
    "/regular/<id>/delete",
    methods=["POST"]
)
def delete_regular_document(id):

    document = (
        Document.query.get_or_404(id)
    )

    db.session.delete(
        document
    )

    db.session.commit()

    return redirect(
        url_for(
            "regular_documents"
        )
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )
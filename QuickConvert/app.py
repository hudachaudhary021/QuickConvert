"""
QuickConvert - Flask Web Application
Word <-> PDF conversion service with drag & drop upload,
file validation, and automatic cleanup of stored files.
"""

import os
import time
import uuid
import threading
import logging
from datetime import datetime

from flask import (
    Flask, render_template, request, send_file,
    redirect, url_for, flash, jsonify, after_this_request
)
from werkzeug.utils import secure_filename

from utils.converter import (
    convert_word_to_pdf,
    convert_pdf_to_word,
    ConversionError,
)
from utils.blog_data import BLOG_POSTS

# --------------------------------------------------------------------------
# App configuration
# --------------------------------------------------------------------------

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
CONVERTED_FOLDER = os.path.join(BASE_DIR, "converted")

ALLOWED_WORD_EXTENSIONS = {"doc", "docx"}
ALLOWED_PDF_EXTENSIONS = {"pdf"}
MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 MB max upload size
FILE_MAX_AGE_SECONDS = 30 * 60  # auto-delete files older than 30 minutes

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "quickconvert-dev-secret-key")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("quickconvert")


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def allowed_file(filename, allowed_extensions):
    """Return True if filename has one of the allowed extensions."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


def unique_path(folder, filename):
    """Build a unique, secure file path inside folder."""
    safe_name = secure_filename(filename)
    name, ext = os.path.splitext(safe_name)
    token = uuid.uuid4().hex[:10]
    return os.path.join(folder, f"{name}_{token}{ext}")


def cleanup_old_files():
    """Delete files older than FILE_MAX_AGE_SECONDS from upload/converted dirs."""
    now = time.time()
    for folder in (UPLOAD_FOLDER, CONVERTED_FOLDER):
        try:
            for fname in os.listdir(folder):
                fpath = os.path.join(folder, fname)
                if fname == ".gitkeep":
                    continue
                if os.path.isfile(fpath):
                    age = now - os.path.getmtime(fpath)
                    if age > FILE_MAX_AGE_SECONDS:
                        try:
                            os.remove(fpath)
                            logger.info("Auto-deleted expired file: %s", fpath)
                        except OSError as exc:
                            logger.warning("Could not delete %s: %s", fpath, exc)
        except FileNotFoundError:
            continue


def background_cleanup_loop():
    """Run cleanup periodically in a background daemon thread."""
    while True:
        cleanup_old_files()
        time.sleep(300)  # every 5 minutes


_cleanup_thread = threading.Thread(target=background_cleanup_loop, daemon=True)
_cleanup_thread.start()


def safe_remove(path):
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except OSError as exc:
        logger.warning("Failed to remove file %s: %s", path, exc)


# --------------------------------------------------------------------------
# Routes - Pages
# --------------------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html", active_page="home")


@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in all fields before sending your message.", "error")
            return redirect(url_for("contact"))

        logger.info("Contact form submitted by %s <%s>", name, email)
        flash("Thanks for reaching out! We'll get back to you soon.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", active_page="contact")


@app.route("/privacy-policy")
def privacy():
    return render_template("privacy.html", active_page="privacy")


@app.route("/terms-and-conditions")
def terms():
    return render_template("terms.html", active_page="terms")


@app.route("/faq")
def faq():
    return render_template("faq.html", active_page="faq")


@app.route("/blog")
def blog():
    return render_template("blog.html", active_page="blog", posts=BLOG_POSTS)


@app.route("/blog/<slug>")
def blog_post(slug):
    post = next((p for p in BLOG_POSTS if p["slug"] == slug), None)
    if post is None:
        return render_template("404.html"), 404
    return render_template("blog_post.html", active_page="blog", post=post)


@app.route("/ads.txt")
def ads_txt():
    """Serve ads.txt at the site root, required by Google AdSense."""
    content = "google.com, pub-3874660214976289, DIRECT, f08c47fec0942fa0\n"
    return app.response_class(content, mimetype="text/plain")


# --------------------------------------------------------------------------
# Routes - Conversion API
# --------------------------------------------------------------------------

@app.route("/convert/word-to-pdf", methods=["POST"])
def word_to_pdf_route():
    cleanup_old_files()

    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part in the request."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    if not allowed_file(file.filename, ALLOWED_WORD_EXTENSIONS):
        return jsonify({
            "success": False,
            "error": "Invalid file type. Only .doc and .docx files are allowed."
        }), 400

    upload_path = unique_path(UPLOAD_FOLDER, file.filename)
    file.save(upload_path)

    output_name = os.path.splitext(os.path.basename(upload_path))[0] + ".pdf"
    output_path = os.path.join(CONVERTED_FOLDER, output_name)

    try:
        convert_word_to_pdf(upload_path, output_path)
    except ConversionError as exc:
        safe_remove(upload_path)
        return jsonify({"success": False, "error": str(exc)}), 422
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error converting Word to PDF")
        safe_remove(upload_path)
        return jsonify({"success": False, "error": "Conversion failed. Please try again."}), 500

    safe_remove(upload_path)

    download_name = os.path.splitext(secure_filename(file.filename))[0] + ".pdf"
    return jsonify({
        "success": True,
        "download_url": url_for("download_file", folder="converted", filename=os.path.basename(output_path)),
        "filename": download_name,
    })


@app.route("/convert/pdf-to-word", methods=["POST"])
def pdf_to_word_route():
    cleanup_old_files()

    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part in the request."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    if not allowed_file(file.filename, ALLOWED_PDF_EXTENSIONS):
        return jsonify({
            "success": False,
            "error": "Invalid file type. Only .pdf files are allowed."
        }), 400

    upload_path = unique_path(UPLOAD_FOLDER, file.filename)
    file.save(upload_path)

    output_name = os.path.splitext(os.path.basename(upload_path))[0] + ".docx"
    output_path = os.path.join(CONVERTED_FOLDER, output_name)

    try:
        convert_pdf_to_word(upload_path, output_path)
    except ConversionError as exc:
        safe_remove(upload_path)
        return jsonify({"success": False, "error": str(exc)}), 422
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error converting PDF to Word")
        safe_remove(upload_path)
        return jsonify({"success": False, "error": "Conversion failed. Please try again."}), 500

    safe_remove(upload_path)

    download_name = os.path.splitext(secure_filename(file.filename))[0] + ".docx"
    return jsonify({
        "success": True,
        "download_url": url_for("download_file", folder="converted", filename=os.path.basename(output_path)),
        "filename": download_name,
    })


@app.route("/download/<folder>/<path:filename>")
def download_file(folder, filename):
    if folder not in ("converted", "uploads"):
        return render_template("404.html"), 404

    directory = CONVERTED_FOLDER if folder == "converted" else UPLOAD_FOLDER
    safe_name = secure_filename(filename)
    file_path = os.path.join(directory, safe_name)

    if not os.path.isfile(file_path):
        return render_template("404.html"), 404

    # Files are cleaned up by the background sweep (every 5 minutes,
    # anything older than 30 minutes) instead of deleting immediately
    # after the first download. This avoids corrupting downloads if a
    # mobile browser retries or re-requests the same file link.
    return send_file(file_path, as_attachment=True)


# --------------------------------------------------------------------------
# Error handlers
# --------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({
        "success": False,
        "error": "File is too large. Maximum upload size is 20 MB."
    }), 413


@app.errorhandler(500)
def server_error(_error):
    return render_template("404.html", server_error=True), 500


@app.context_processor
def inject_globals():
    return {"current_year": datetime.utcnow().year}


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
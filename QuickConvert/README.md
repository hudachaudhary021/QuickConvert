# QuickConvert

QuickConvert is a fast, free, and secure web app for converting **Word documents to PDF** and **PDF files back to Word**, built with Flask, HTML5, CSS3, and vanilla JavaScript. It features a responsive glassmorphism UI, drag-and-drop uploads, strict file validation, and automatic deletion of every uploaded/converted file.

---

## Features

- 📄 Word (.doc/.docx) → PDF conversion
- 📄 PDF → Word (.docx) conversion
- 🖱️ Drag & drop upload with click-to-browse fallback
- ✅ Client-side and server-side file validation (type + size, 20MB max)
- 🗑️ Automatic deletion of uploaded and converted files (background cleanup + post-download deletion)
- 💎 Glassmorphism UI, fully responsive (mobile, tablet, laptop, desktop)
- 📃 Pages: Home, About, Contact, Privacy Policy, Terms & Conditions, FAQ, and a custom 404 page

---

## Project structure

```
QuickConvert/
├── app.py                   # Flask application & routes
├── requirements.txt          # Python dependencies
├── Procfile                  # Render/Heroku start command
├── runtime.txt                # Python version pin
├── README.md
├── .gitignore
├── utils/
│   ├── __init__.py
│   └── converter.py          # Word<->PDF conversion logic
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── contact.html
│   ├── privacy.html
│   ├── terms.html
│   ├── faq.html
│   └── 404.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── img/logo.svg
├── uploads/                  # Temporary uploads (auto-cleaned, gitignored)
└── converted/                 # Temporary converted output (auto-cleaned, gitignored)
```

---

## Run on Termux (Android) — one single command

Install Termux from F-Droid (recommended) or Google Play, open it, then paste this **single command** (it installs everything and starts the server):

```bash
pkg update -y && pkg upgrade -y && pkg install -y python git libjpeg-turbo libxml2 libxslt clang && pip install --upgrade pip && (test -d QuickConvert || git clone https://github.com/YOUR-USERNAME/QuickConvert.git) && cd QuickConvert && pip install -r requirements.txt && python app.py
```

Then open your phone's browser and go to:

```
http://127.0.0.1:5000
```

> If you're setting up from a local copy instead of GitHub, just place the `QuickConvert` folder inside Termux's home directory first, `cd` into it, then run:
> `pkg update -y && pkg install -y python libjpeg-turbo libxml2 libxslt clang && pip install --upgrade pip && pip install -r requirements.txt && python app.py`

---

## Run locally (Windows / macOS / Linux)

```bash
git clone https://github.com/YOUR-USERNAME/QuickConvert.git
cd QuickConvert
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## Deploy to Render

1. Push this project to a GitHub repository.
2. On [Render](https://render.com), create a **New Web Service** and connect your repo.
3. Render will detect `Procfile` and `runtime.txt` automatically. Use these settings if asked:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Set an environment variable `SECRET_KEY` to a long random string (Render → Environment tab).
5. Deploy. Render will give you a live URL such as `https://quickconvert.onrender.com`.

---

## Deploy to GitHub

```bash
git init
git add .
git commit -m "Initial commit: QuickConvert"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/QuickConvert.git
git push -u origin main
```

---

## Environment variables

| Variable     | Description                                | Default                    |
|--------------|---------------------------------------------|----------------------------|
| `SECRET_KEY` | Flask session/flash secret key               | dev key (change in prod)   |
| `PORT`       | Port the app listens on                      | `5000`                     |
| `FLASK_DEBUG`| Enable/disable debug mode (`true`/`false`)   | `true`                      |

---

## How conversion works

- **Word → PDF**: reads the `.docx` with `python-docx` (paragraphs, headings, lists, tables, bold/italic/underline) and renders it into a PDF with `reportlab`. No LibreOffice or MS Word required — works on Termux and Render.
- **PDF → Word**: uses `pdf2docx`, which parses the PDF layout directly and reconstructs a native `.docx` file — also no external binaries required.

---

## File validation & auto-delete

- Uploads are restricted to `.doc`/`.docx` (for Word→PDF) or `.pdf` (for PDF→Word), max **20MB**.
- Every uploaded file is deleted immediately after conversion.
- Converted files are deleted a few seconds after being downloaded.
- A background thread also sweeps the `uploads/` and `converted/` folders every 5 minutes, removing anything older than 30 minutes as a safety net.

---

## License

This project is provided as-is for personal and commercial use.

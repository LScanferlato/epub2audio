from flask import Flask, render_template, request, send_from_directory
import os
import subprocess
import threading
import json

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app = Flask(__name__)


# -----------------------------
#   CONVERSIONE IN THREAD
# -----------------------------
def run_conversion(epub_path, prefix, language, model):
    subprocess.run(["python", "convert.py", epub_path, prefix, language, model])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        prefix = request.form.get("prefix", "output")
        language = request.form.get("language")
        model = request.form.get("model")

        epub_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(epub_path)

        thread = threading.Thread(target=run_conversion, args=(epub_path, prefix, language, model))
        thread.start()

        return render_template("progress.html")

    return render_template("index.html")


@app.route("/progress")
def progress():
    try:
        with open("progress.json") as f:
            return json.load(f)
    except:
        return {"current": 0, "total": 1}


@app.route("/audio")
def list_audio():
    files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(".wav")]
    return render_template("audio_list.html", files=files)


@app.route("/audio/<path:filename>")
def download_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

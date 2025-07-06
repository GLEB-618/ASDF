from flask import render_template, request
from app import app
from .minio_client import save_video


@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']
    filename = file.filename

    save_video(file, filename)

    return f"Загружено: /videos/{filename}"
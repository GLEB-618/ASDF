from flask import render_template, request, jsonify
from app import app
from .minio_client import upload_video
import uuid, tempfile, pyclamd, os


@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Получаем файл из формы (multipart/form-data)
    file = request.files.get('video')
    if not file:
        return jsonify({'error': 'No video uploaded'}), 400

    # Подключение к clamd
    cd = pyclamd.ClamdNetworkSocket(host='26.176.35.255', port=3310)

    if not cd.ping():
        return jsonify({'error': 'ClamAV daemon is not available'}), 500
    
    # Перемещаем указатель в начало и скармливаем байты
    file.seek(0)
    result = cd.scan_stream(file.read())
    if result is not None:
        return jsonify({'error': 'File is infected', 'details': result}), 400

    file.seek(0)
    upload_video(file, file.filename)

    # Возвращаем ID видео
    return jsonify({'message': 'Upload successful'}), 200
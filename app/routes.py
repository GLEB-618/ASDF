from flask import  Flask, render_template, request, jsonify
from app import app
from .minio_client import upload_video
import pyclamd, uuid
from data.orm import SyncORM


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/liking")
def liking():
    return render_template('liking.html')

@app.route("/settings")
def setting():
    return render_template('settings.html')

@app.route("/info")
def info():
    return render_template('info.html')

@app.route("/help")
def help():
    return render_template('help.html')

@app.route("/complaints")
def complaints():
    return render_template('complaints.html')

@app.route("/channel")
def channel():
    return render_template('channel.html')

@app.route('/upload')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Получаем файл из формы (multipart/form-data)
    title = request.form.get('title')
    description = request.form.get('description')
    file = request.files.get('video')
    if not file:
        return jsonify({'error': 'No video uploaded'}), 400

    # Подключение к clamd
    cd = pyclamd.ClamdNetworkSocket(host='26.48.28.173', port=3310)

    if not cd.ping():
        return jsonify({'error': 'ClamAV daemon is not available'}), 500
    
    # Перемещаем указатель в начало и скармливаем байты
    file.seek(0)
    result = cd.scan_stream(file.read())
    if result is not None:
        return jsonify({'error': 'File is infected', 'details': result}), 400

    file.seek(0)
    # Генерим уникальный ID
    uid = uuid.uuid4().hex
    upload_video(file, file.filename, uid)
    SyncORM.insert_meta_video(uid, title, description) # type: ignore

    # Возвращаем ID видео
    return jsonify({'message': 'Upload successful'}), 200

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")
import os, tempfile, ffmpeg
from minio import Minio
from flask import current_app, jsonify
from datetime import timedelta

def get_s3_client():
    client = Minio(
        current_app.config['AWS_S3_ENDPOINT_URL'],
        access_key=current_app.config['AWS_ACCESS_KEY_ID'],
        secret_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        secure=False
    )
    return client

def upload_video(file_obj, filename, uid):
    s3 = get_s3_client()

    # Сохраняем оригинал во временный файл
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, filename)
        file_obj.save(input_path)

        # Путь для mp4-файла
        mp4_filename = f"{uid}.mp4"
        output_path = os.path.join(temp_dir, mp4_filename)

        # Конвертация через ffmpeg
        try:
            (
                ffmpeg
                .input(input_path)
                .output(output_path,
                        vcodec='libx264',
                        acodec='aac',
                        # preset='slow',
                        # crf=20,
                        # movflags='faststart',
                        # max_muxing_queue_size=1024
                        )
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError("Ошибка ffmpeg:\n" + e.stderr.decode())

        # Загрузка в MinIO
        s3.fput_object(
            bucket_name=current_app.config['AWS_BUCKET_NAME'],
            object_name=mp4_filename,
            file_path=output_path,
            content_type='video/mp4'
        )

        # Возвращаем имя сконвертированного файла
        return mp4_filename
    
def get_url_video(video_id):
    s3 = get_s3_client()
    presigned_url = s3.presigned_get_object("videos", video_id + ".mp4", expires=timedelta(hours=1))
    return jsonify({"url": presigned_url})
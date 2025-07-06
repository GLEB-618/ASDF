import os
import tempfile
import ffmpeg
import boto3
from botocore.client import Config
from flask import current_app

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=current_app.config['AWS_S3_ENDPOINT_URL'],
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )

def save_video(file_obj, filename):
    s3 = get_s3_client()

    # Сохраняем оригинал во временный файл
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, filename)
        file_obj.save(input_path)

        # Путь для mp4-файла
        if filename.lower().endswith('.mp4'):
            mp4_filename = os.path.splitext(filename)[0] + '_reencoded.mp4'
        else:
            mp4_filename = os.path.splitext(filename)[0] + '.mp4'
        output_path = os.path.join(temp_dir, mp4_filename)

        # Конвертация через ffmpeg
        try:
            (
                ffmpeg
                .input(input_path)
                .output(output_path,
                        vcodec='libx264',
                        acodec='aac',
                        preset='slow',
                        crf=20,
                        movflags='faststart',
                        max_muxing_queue_size=1024)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
        except ffmpeg.Error as e:
            raise RuntimeError("Ошибка ffmpeg:\n" + e.stderr.decode())

        # Загрузка в MinIO
        with open(output_path, 'rb') as converted_file:
            s3.upload_fileobj(converted_file, current_app.config['AWS_BUCKET_NAME'], mp4_filename)

        # Возвращаем имя сконвертированного файла
        return mp4_filename
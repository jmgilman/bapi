import boto3
import os

from pathlib import Path


def download(bucket: str, key: str, path: str):
    s3 = boto3.resource("s3").Bucket(bucket)
    file_path = os.path.join(path, key)
    file_dir = os.path.dirname(file_path)

    Path(file_dir).mkdir(parents=True, exist_ok=True)
    s3.download_file(key, file_path)


def download_all(bucket: str, path: str):
    s3 = boto3.resource("s3").Bucket(bucket)
    for object in s3.objects.all():
        download(bucket, object.key, path)

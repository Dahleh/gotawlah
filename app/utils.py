from passlib.context import CryptContext
from fastapi import UploadFile
from typing import List
import boto3
from .config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def upload_image(file: UploadFile):
    s3 = boto3.resource('s3',aws_access_key_id=settings.aws_access_key_id,
         aws_secret_access_key= settings.aws_secret_access_key)
    s3.Bucket(settings.bucket_name).upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})
    return f'https://{settings.bucket_name}.s3.amazonaws.com/{file.filename}'


def upload_multi_images(files: List[UploadFile]):
    images = []
    s3 = boto3.resource('s3',aws_access_key_id=settings.aws_access_key_id,
         aws_secret_access_key= settings.aws_secret_access_key)
    for file in files:
        s3.Bucket(settings.bucket_name).upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})
        images.append(f'https://{settings.bucket_name}.s3.amazonaws.com/{file.filename}')

    return images
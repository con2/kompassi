from urllib.parse import unquote, urlparse

import boto3
from django.conf import settings

BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
S3_ENDPOINT_URL = settings.AWS_S3_ENDPOINT_URL
S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=S3_ENDPOINT_URL,
)


def is_valid_s3_url(url: str):
    bucket_url = f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/"
    return url.startswith(bucket_url)


def presign_get(url: str):
    bucket_url = f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/"

    if not url.startswith(bucket_url):
        raise ValueError("URL must be a valid S3 URL in our known bucket")

    key = url.removeprefix(bucket_url)

    return S3_CLIENT.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": key,
        },
        ExpiresIn=3600,
    )


def presign_put(filename: str, file_type: str):
    return S3_CLIENT.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": filename,
            "ContentType": file_type,
        },
        ExpiresIn=3600,
    )


def satanize_presigned_url(presigned_url: str):
    parsed = urlparse(presigned_url)
    path = unquote(parsed.path.rstrip("/"))
    if not path:
        raise ValueError("presigned_url is sus:", repr(presigned_url))
    return path.split("/")[-1]

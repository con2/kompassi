from base64 import urlsafe_b64encode
from os import urandom
from os.path import splitext

import boto3
import graphene
from django.conf import settings

bucket_name = settings.AWS_STORAGE_BUCKET_NAME
s3_endpoint_url = settings.AWS_S3_ENDPOINT_URL
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url=s3_endpoint_url,
)


def generate_unique_id():
    buffer = urandom(8)
    return urlsafe_b64encode(buffer).decode("utf-8").rstrip("=")


class InitFileUploadInput(graphene.InputObjectType):
    filename = graphene.String(required=True)
    file_type = graphene.String(required=True)


class InitFileUploadResponse(graphene.ObjectType):
    upload_url = graphene.String()
    file_url = graphene.String()


class InitFileUpload(graphene.Mutation):
    class Arguments:
        input = InitFileUploadInput(required=True)

    Output = InitFileUploadResponse

    @staticmethod
    def mutate(root, info, input):
        file_type = input.file_type

        name, extension = splitext(input.filename)
        filename = f"{name}.{generate_unique_id()}{extension}"

        presigned_url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": bucket_name,
                "Key": filename,
                "ContentType": file_type,
            },
            ExpiresIn=3600,
        )
        object_url = f"{s3_endpoint_url}/{bucket_name}/{filename}"
        return InitFileUploadResponse(upload_url=presigned_url, file_url=object_url)

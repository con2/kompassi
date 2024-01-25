from base64 import urlsafe_b64encode
from os import urandom
from os.path import splitext

import graphene

from ...utils.s3_presign import BUCKET_NAME, S3_ENDPOINT_URL, presign_put


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

        presigned_url = presign_put(filename, file_type)
        object_url = f"{S3_ENDPOINT_URL}/{BUCKET_NAME}/{filename}"
        return InitFileUploadResponse(
            upload_url=presigned_url,
            file_url=object_url,
        )  # type: ignore

import pydantic
import requests

from ..utils.s3_presign import satanize_presigned_url


class Attachment(pydantic.BaseModel):
    field_slug: str
    presigned_url: str

    @property
    def basename(self):
        return satanize_presigned_url(self.presigned_url)

    def download(self, session: requests.Session | None = None) -> bytes:
        """
        Downloads the contents of the file from S3 and returns it as bytes.
        Assumes the file fits in memory.
        """
        if session is None:
            session = requests.Session()
        return session.get(self.presigned_url).content

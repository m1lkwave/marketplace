import aioboto3
from typing import BinaryIO

from src.storage.base import Storage

class S3Storage(Storage):

    def __init__(
            self,
            endpoint_url: str,
            aws_access_key_id: str,
            aws_secret_access_key: str,
            bucket: str,
    ):
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.session = aioboto3.Session()
        self.bucket = bucket

    async def upload(
            self, 
            file: BinaryIO, 
            key: str, 
            content_type: str,
        ) -> str:
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        ) as client:
            await client.upload_fileobj(
                Fileobj=file,
                Bucket=self.bucket,
                Key=key,
                ExtraArgs={"ContentType": content_type}
            )
        return key

    async def delete(
            self,
            key: str,
    ) -> None:
        async with self.session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as client:
            await client.delete_object(
                Bucket=self.bucket,
                Key=key,
            )
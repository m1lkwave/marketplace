from src.storage.base import Storage
from src.storage.s3 import S3Storage
from src.settings import settings

def get_storage() -> Storage:
    s3 = S3Storage(
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        bucket=settings.s3_bucket
    )
    return s3
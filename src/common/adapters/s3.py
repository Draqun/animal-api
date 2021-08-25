import logging
import os
from typing import Tuple
from uuid import uuid4

from mypy_boto3_s3 import S3Client
from werkzeug.datastructures import FileStorage

from common.ports.aws import get_s3_client


class S3NotAllowedObjectType(Exception):
    pass


class S3UploadFailed(Exception):
    pass


class S3:
    INCOMING_BUCKET = os.environ['S3_BUCKET_INCOMING_FILES_NAME']

    def __init__(self):
        self._client: S3Client = get_s3_client()

    @staticmethod
    def is_allowed_type(image_type: str) -> bool:
        return image_type in ['image/png', 'image/jpeg']

    def upload_image(self, image: FileStorage) -> Tuple[str, str]:
        if not self.is_allowed_type(image.content_type):
            raise S3NotAllowedObjectType()

        ext = image.filename.split('.')[-1] if image.filename else image.content_type.split('/')[-1]
        key = uuid4().hex + '.' + ext
        try:
            self._client.put_object(
                Body=image.stream, Bucket=self.INCOMING_BUCKET, Key=key, ContentType=image.content_type
            )
        except self._client.exceptions.ClientError as ex:
            logging.exception(ex)
            logging.error(f'Error putting object {key} to bucket {self.INCOMING_BUCKET}.')
            raise S3UploadFailed from None

        return key, self.INCOMING_BUCKET

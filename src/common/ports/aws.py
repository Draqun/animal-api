from functools import lru_cache
import logging
import os

from boto3.session import Session
from botocore.config import Config
from mypy_boto3_s3 import S3Client


BOTO_CONFIG = Config(retries={'mode': 'standard'})


@lru_cache(maxsize=None)
def get_session() -> Session:
    logging.info('Creating new boto3 session')
    return Session()


@lru_cache(maxsize=None)
def get_s3_client() -> S3Client:
    logging.info('Creating S3 client')
    aws_s3_url = os.environ.get('AWS_S3_URL', 'https://s3.amazonaws.com')
    aws_region = os.environ.get('AWS_REGION', 'eu-west-1')

    return get_session().client(
        service_name='s3',
        region_name=aws_region,
        endpoint_url=aws_s3_url,
        config=BOTO_CONFIG,
    )

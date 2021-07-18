import logging
import os
from typing import Optional, Tuple
from uuid import uuid4

import boto3
from sqlalchemy import create_engine, text
from werkzeug.datastructures import FileStorage

from api.webapp.settings import config


incoming_bucket = os.environ['S3_BUCKET_INCOMING_FILES_NAME']
aws_s3_url = os.environ.get('AWS_S3_URL', 'https://s3.amazonaws.com')
aws_s3_url = aws_s3_url.replace('https://', f'https://{incoming_bucket}/')


def is_allowed_type(image_type: str) -> bool:
    return image_type in ['image/png', 'image/jpeg']


def add_animal(body, image: Optional[FileStorage] = None) -> Tuple[dict, int]:
    key = ''

    if image is not None:
        if not is_allowed_type(image.content_type):
            return {'status': 'Incorrect file content'}, 415

        try:
            s3 = boto3.client('s3', endpoint_url=aws_s3_url)
            key = uuid4().hex + '.' + image.filename.split(".")[-1]
            s3.put_object(Body=image, Bucket=incoming_bucket, Key=key, ContentType=image.content_type)
        except Exception as ex:  # pylint: disable=broad-except
            logging.exception(ex)
            logging.error('Error putting object {} to bucket {}.'.format(key, incoming_bucket))
            return {'status': 'File upload failed'}, 415

    if key:
        body['image'] = f'{aws_s3_url}/{key}'

    db_eng = create_engine(config.connection_string, echo=True)
    with db_eng.begin() as conn:
        try:
            result = conn.execute(
                text("INSERT INTO animals (name, description, image_url) VALUES (:name, :description, :image);"),
                body
            )
        except Exception as ex:
            logging.exception(ex)
            return {'status': 'Incorrect values', 'values': body}, 405

    body['id'] = result.lastrowid
    return body, 201


def animals() -> Tuple[list, int]:
    db_eng = create_engine(config.connection_string, echo=True)
    items = []
    with db_eng.begin() as conn:
        try:
            result = conn.execute(
                text("SELECT * FROM animals"),
            )
        except Exception as ex:
            logging.exception(ex)
        else:
            for item in result:
                item = dict(item)
                if ('image_url' in item) and item['image_url'] is not None:
                    item['image'] = item.pop('image_url')
                items.append(item)

    return items, 200

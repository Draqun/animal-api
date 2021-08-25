from typing import Optional, Tuple

from werkzeug.datastructures import FileStorage

from api.webapp.settings import config
from common.adapters.repository.animal import Animal
from common.adapters.repository.db.unit_of_work import SQLUnitOfWork
from common.adapters.s3 import S3, S3NotAllowedObjectType, S3UploadFailed


def add_animal(body, image: Optional[FileStorage] = None) -> Tuple[dict, int]:
    data = {}
    data.update(body)
    if image is not None:
        try:
            data['image_key'], data['bucket_name'] = S3().upload_image(image)
        except S3NotAllowedObjectType:
            return {'status': 'Incorrect file content'}, 415
        except S3UploadFailed:
            return {'status': 'File upload failed'}, 415
    with SQLUnitOfWork(config) as uow:
        animal = Animal(**data).add_animal_to_db(uow)
        if not animal:
            return {'status': 'Incorrect values', 'values': body}, 405

    return animal.as_dict(), 201


def animals() -> Tuple[list, int]:
    with SQLUnitOfWork(config) as uow:
        return Animal.all(uow), 200

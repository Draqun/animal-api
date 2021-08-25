from __future__ import annotations

from typing import List, Optional, cast

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from common.ports.aws import get_s3_client
from common.ports.repository.unit_of_work import UnitOfWork

BaseModel = declarative_base()


class Animal(BaseModel):
    __tablename__ = 'animals'

    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column('name', sa.String(100), nullable=False)
    description = sa.Column('description', sa.Unicode(1024))
    image_key = sa.Column('image_key', sa.String(128), nullable=True)
    bucket_name = sa.Column('bucket_name', sa.String(128), nullable=True)

    def as_dict(self):
        animal = self.__dict__
        del animal['_sa_instance_state']
        animal['image'] = self.image
        return animal

    @property
    def image(self) -> Optional[str]:
        if (self.bucket_name is None) or (self.image_key is None):
            return None

        return get_s3_client().generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': self.bucket_name, 'Key': self.image_key},
        )

    def add_animal_to_db(self, uow: UnitOfWork) -> Animal:
        animal = uow.add(self, flush=True)
        uow.commit()
        return cast(Animal, animal)

    @staticmethod
    def all(uow: UnitOfWork) -> List[Animal]:
        return [animal.as_dict() for animal in uow.query(Animal).all()]

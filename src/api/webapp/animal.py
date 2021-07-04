from typing import Tuple

from sqlalchemy import create_engine, text

from api.webapp.settings import config

def add_animal(body) -> Tuple[dict, int]:
    db_eng = create_engine(config.connection_string, echo=True)
    with db_eng.begin() as conn:
        try:
            result = conn.execute(
                text("INSERT INTO animals (name, description) VALUES (:name, :description);"),
                body
            )
        except Exception:
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
        except Exception:
            pass
        else:
            for a in result:
                items.append(
                    dict(a)
                )

    return items, 200

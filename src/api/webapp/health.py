from typing import Tuple


def health() -> Tuple[dict, int]:
    return {'status': 'alive'}, 200

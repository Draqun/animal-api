from gevent.monkey import patch_all

# must patch before importing anything else - https://github.com/gevent/gevent/issues/1016
patch_all()  # pylint: disable=wrong-import-position

from api.webapp.app import app  # pylint: disable=unused-import

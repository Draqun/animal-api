#!/bin/bash

/opt/upskill_backend/venv/bin/gunicorn --pythonpath /opt/upskill_backend/src --chdir /opt/upskill_backend/src/api/webapp --log-level INFO --worker-class gevent --workers `nproc` --bind unix:upskill_backend.sock -m 007 gunicorn_entrypoint:app

# Makefile

SHELL := /bin/bash
PROJECT = UPSKILL
PY_VERSION = python3.8
DEV_DB_ENV_VARIABLES=MIGRATION_ENV=local DB_WRITER_HOST=127.0.0.1 DB_READER_HOST=127.0.0.1 DB_HOST=127.0.0.1 DB_PORT=3306 DB_NAME=db DB_USER=user DB_PASSWORD=pass DB_PASSWORD_TYPE=local
DEV_SERVICES_ENV_VARIABLES=$(DEV_DB_ENV_VARIABLES)
WORKERS_PER_CORE=1
NB_OF_CORES := $(shell nproc)

APP_HOST := 0.0.0.0
APP_PORT := 8000
APP_LOG_LEVEL := INFO

ifneq (,$(wildcard environment.env))
	include environment.env
	export $(shell sed 's/=.*//' environment.env)
endif

source-env:
	source ./venv/bin/activate

init-env:
	$(PY_VERSION) -m venv venv

create-env: init-env source-env
	pip install -r requirements.txt

freeze: source-env
	pip freeze > requirements.txt

dev-env-up: source-env
	${DEV_SERVICES_ENV_VARIABLES} docker-compose -p ${PROJECT} -f docker/docker-compose.yaml up -d --build --remove-orphans
	@while [ $$(docker ps --filter health=starting --format "{{.Status}}" | wc -l) != 0 ]; do echo 'waiting for healthy containers'; sleep 1; done
	${DEV_SERVICES_ENV_VARIABLES} $(MAKE) schema-upgrade

dev-env-down:
	${DEV_SERVICES_ENV_VARIABLES} docker-compose -p ${PROJECT} -f docker/docker-compose.yaml down -v --remove-orphans

schema-upgrade:
	cd db-migrations; alembic -x env=${MIGRATION_ENV} upgrade head

run-gunicorn:
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" gunicorn --bind $(APP_HOST):$(APP_PORT) \
		--workers=$$(( $(WORKERS_PER_CORE) * $(NB_OF_CORES) )) \
		--chdir src/api/webapp/ gunicorn_entrypoint:app \
		--log-level ${APP_LOG_LEVEL} \
		--worker-class gevent
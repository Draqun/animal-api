# Makefile

SHELL := /bin/bash
PROJECT = UPSKILL
PY_VERSION = python3.8
DEV_DB_ENV_VARIABLES=MIGRATION_ENV=local DB_WRITER_HOST=127.0.0.1 DB_READER_HOST=127.0.0.1 DB_HOST=127.0.0.1 DB_PORT=3306 DB_NAME=db DB_USER=user DB_PASSWORD=pass DB_PASSWORD_TYPE=local
DEV_SERVICES_ENV_VARIABLES=$(DEV_DB_ENV_VARIABLES)


source-env:
	source $(PWD)/venv/bin/activate

init-env:
	$(PY_VERSION) -m venv venv

create-env: init-env source-env
	pip install -r requirements.txt

freeze: source-env
	pip freeze > requirements.txt

dev-services-up-env: source-env
	${DEV_SERVICES_ENV_VARIABLES} docker-compose -p ${PROJECT} -f docker/docker-compose.yaml up -d --build --remove-orphans
	@while [ $$(docker ps --filter health=starting --format "{{.Status}}" | wc -l) != 0 ]; do echo 'waiting for healthy containers'; sleep 1; done
	${DEV_SERVICES_ENV_VARIABLES} $(MAKE) schema-upgrade

dev-services-down:
	${DEV_SERVICES_ENV_VARIABLES} docker-compose -p ${PROJECT} -f docker/docker-compose.yaml down -v --remove-orphans

schema-upgrade:
	cd db-migrations; alembic -x env=${MIGRATION_ENV} upgrade HEAD
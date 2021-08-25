# Makefile

SHELL := /usr/bin/env bash
PROJECT = UPSKILL
ifeq ($(OS), Windows_NT)
	PY_VERSION = python.exe
else
	PY_VERSION = python3.9
endif
DEV_DB_ENV_VARIABLES=MIGRATION_ENV=local DB_WRITER_HOST=127.0.0.1 DB_READER_HOST=127.0.0.1 DB_HOST=127.0.0.1 DB_PORT=3306 DB_NAME=db DB_USER=user DB_PASSWORD=pass DB_PASSWORD_TYPE=local
DEV_SERVICES_ENV_VARIABLES=$(DEV_DB_ENV_VARIABLES)
WORKERS_PER_CORE=1
NB_OF_CORES := $(shell nproc)
VENV_DIR ?= venv
PIP_CMD ?= pip

APP_HOST := 0.0.0.0
APP_PORT := 8000
APP_LOG_LEVEL := INFO

ifneq (,$(wildcard environment.env))
	include environment.env
	export $(shell sed 's/=.*//' environment.env)
endif

VENV_RUN = $(VENV_DIR)/bin/activate

source-env:
ifeq ($(OS), Windows_NT)
	echo "On Windows platform venv has to be sourced manually"
else
	source $(VENV_RUN)
endif

init-env:
	(test `which virtualenv` || $(PIP_CMD) install --user virtualenv) && \
		(test -e $(VENV_DIR) || virtualenv $(VENV_OPTS) $(VENV_DIR)) && \
		($(PY_VERSION) -m pip install --upgrade pip)

create-env: source-env
	test ! -e requirements.txt || $(PIP_CMD) -q install -r requirements.txt

freeze: source-env
	$(PIP_CMD) freeze > requirements.txt

dev-env-up: source-env
	docker volume create --name=db-data
	${DEV_SERVICES_ENV_VARIABLES} docker compose -p ${PROJECT} -f docker/docker-compose.yaml up -d --build --remove-orphans
	@while [ $$(docker ps --filter health=starting --format "{{.Status}}" | wc -l) != 0 ]; do echo 'waiting for healthy containers'; sleep 1; done
	${DEV_SERVICES_ENV_VARIABLES} make schema-upgrade

dev-env-down:
	${DEV_SERVICES_ENV_VARIABLES} docker compose -p ${PROJECT} -f docker/docker-compose.yaml down -v --remove-orphans

dev-env-clean: dev-env-down
	docker volume remove db-data

schema-upgrade: source-env
	cd db-migrations; (alembic -x env=${MIGRATION_ENV} upgrade head)

new-revision: source-env
	cd db-migrations; (alembic -x env=${MIGRATION_ENV} revision)

run-gunicorn:
	PYTHONPATH="${PYTHONPATH}:${PWD}/src" gunicorn --bind $(APP_HOST):$(APP_PORT) \
		--workers=$$(( $(WORKERS_PER_CORE) * $(NB_OF_CORES) )) \
		--chdir src/api/webapp/ gunicorn_entrypoint:app \
		--log-level ${APP_LOG_LEVEL} \
		--worker-class gevent

run-static-analysis-src: source-env
	pylint --rcfile=.cicd/config/pylint src/
	bandit -c=.cicd/config/bandit.config -r src/
	mypy --show-error-codes --config-file .cicd/config/mypy.ini src/

run-static-analysis: run-static-analysis-src
include .env

up:
	@echo 'Iniciando Docker e subindo serviços...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env up

up_d:
	@echo 'Iniciando Docker e subindo serviços...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env up -d

rebuild:
	@echo 'Fazendo build do Docker compose...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env build --no-cache
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env up

build:
	@echo 'Fazendo build do Docker compose...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env build --no-cache

stop:
	@echo 'Parando serviços Docker...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env stop

logs:
	@echo 'Logs Docker...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env logs --tail=100

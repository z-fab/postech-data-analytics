DOCKER_FILE = docker/compose.yaml
DOCKER_PROJECT = tc3

up:
	@echo 'Iniciando Docker e subindo serviços...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env up -d
build:
	@echo 'Fazendo build do Docker compose...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env build
stop:
	@echo 'Parando serviços Docker...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env stop
restart:
	@echo 'Reiniciando Docker...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env stop
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env up -d
logs:
	@echo 'Logs Docker...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env logs --tail=100
ps:
	@echo 'Listando Containers Docker...'
	docker compose -p ${DOCKER_PROJECT} -f ${DOCKER_FILE} --env-file .env ps

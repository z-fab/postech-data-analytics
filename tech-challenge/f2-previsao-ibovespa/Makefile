DOCKER_FILE = docker/compose.local.yaml

up:
	@echo 'Iniciando Docker e subindo serviços...'
	docker-compose -f ${DOCKER_FILE} --env-file ./.env up -d
build:
	@echo 'Fazendo build do Docker compose...'
	docker compose -f ${DOCKER_FILE} --env-file ./.env build
stop:
	@echo 'Parando serviços Docker...'
	docker compose -f ${DOCKER_FILE} --env-file ./.env stop
restart:
	@echo 'Reiniciando Docker...'
	docker compose -f ${DOCKER_FILE} --env-file ./.env stop
	docker compose -f ${DOCKER_FILE} --env-file ./.env up -d
logs:
	@echo 'Logs Docker...'
	docker compose -f ${DOCKER_FILE} --env-file ./.env logs --tail=100 -f
ps:
	@echo 'Listando Containers Docker...'
	docker compose -f ${DOCKER_FILE} --env-file ./.env ps
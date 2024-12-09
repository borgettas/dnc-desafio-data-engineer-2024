run:
	echo "AIRFLOW_UID=$$(id -u)" > docker/.env

	mkdir -p logs/
	sudo chmod 777 -R logs
	docker compose -f docker/docker-compose.yaml up --build

down:
	docker compose -f docker/docker-compose.yaml down
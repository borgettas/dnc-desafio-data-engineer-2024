run:
	echo "AIRFLOW_UID=$$(id -u)" > docker/.env
	echo "USER=postgres" >> docker/.env
	echo "PASSWORD=postgres" >> docker/.env
	echo "PORT=5432" >> docker/.env
	echo "HOST=datawarehouse" >> docker/.env
	echo "GOOGLE_API_KEY=" >> docker/.env

	mkdir -p logs/
	sudo chmod 777 -R logs
	docker compose -f docker/docker-compose.yaml up --build

down:
	docker compose -f docker/docker-compose.yaml down
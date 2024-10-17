# YappDown
A note taking app built in Django on Alpine linux with Mariadb using Docker.

to run:
docker build -t yappdown . --network=host
docker run -d -p 8000:8000 --name yappdown-container yappdown

to stop:
docker stop yappdown-container
docker rm yappdown-container

to check logs:
docker logs yappdown-container
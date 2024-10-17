# YappDown
A note taking app built in Django on Alpine linux with Mariadb using Docker.

## Using yappdown.sh (recommended)
```sh
chmod +x yappdown.sh
./yappdown.sh
```

##Manuelly
### to run:
```sh
docker build -t yappdown . --network=host
docker run -d -p 8000:8000 --name yappdown-container yappdown
```

### to stop:
```sh
docker stop yappdown-container
docker rm yappdown-container
```

### to check logs:
```sh
docker logs yappdown-container
```
# YappDown
A note taking app built in Django on Alpine Linux with Mariadb using Docker.

## Using yappdown.sh (recommended)
```sh
chmod +x yappdown.sh
./yappdown.sh
```

## Manually
### Run:
```sh
docker build -t yappdown . --network=host
docker run -d -p 8000:8000 --name yappdown-container yappdown
```

### Stop:
```sh
docker stop yappdown-container
docker rm yappdown-container
```

### Check logs:
```sh
docker logs yappdown-container
```
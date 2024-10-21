# YappDown
A note taking app built in Django on Alpine Linux with Mariadb, SvelteJS and TailwindCSS using Docker.

### Required
Alpine Linux
Django
Mariadb
Docker

### Personal choices
#### SvelteJS
##### Compiles in vanila JavaScript:
Makes fast and efficient frontend.
#### TailwindCSS
##### Fast styling

## Compile and Run
### Automatically (recommended)
#### Linux:
```sh
chmod +x yappdown.sh
./yappdown.sh
```

### Manually compile 
#### Run:
```sh
docker build -t yappdown . --network=host
docker run -d -p 8000:8000 --name yappdown-container yappdown
```

#### Stop:
```sh
docker stop yappdown-container
docker rm yappdown-container
```

#### Check logs:
```sh
docker logs yappdown-container
```
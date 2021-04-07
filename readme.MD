
# Run Docker

## Setup

cd app

docker build -t csv2pdv:0.1 .

docker run -d -p 8500:3800 csv2pdv:0.1


## Management (Using docker-compose)

#### Startup
docker-compose up -d

#### Other Operations
docker-compose up [-d] [--build]
docker-compose down



## Management (Using Docker)

#### List Running Containers
docker ps

#### List All Containers
docker ps -a

#### List Images
docker ps -a

#### Stop Container
docker stop [container]

#### Remove Container
docker rm [container] [-f to force]

#### Remove Image
docker rmi [image]

#### Run Bash
docker exec -it [container] bash

### Clean
docker system prune

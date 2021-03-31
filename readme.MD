
# Run Docker

# Setup

cd app

docker build -t csv2pdv:0.1 .

docker run -d -p 8500:3800 csv2pdv:0.1




## Management

docker stop [container]

docker rm [container] [-f to force]

docker rmi [image]

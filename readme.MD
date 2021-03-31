
# Run Docker

cd app
docker build -t csv2pdv:0.1 .
docker run -d -p 8500:3800 csv2pdv:0.1
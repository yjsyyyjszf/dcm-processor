#!/bin/bash

docker-compose stop $1
docker-compose rm $1

docker rmi "power-worker-scheduler_$1"

docker-compose build $1

docker-compose up -d $1
#!/bin/bash

docker-compose down

docker-compose up -d redis_server orthanc scheduler

sleep 5

if [ -z "$1" ]
then
  docker-compose up -d
else
  docker-compose up $1 -d
fi
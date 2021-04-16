#!/bin/bash

docker-compose down

docker-compose up -d redis_server orthanc scheduler

sleep 5

docker-compose up -d
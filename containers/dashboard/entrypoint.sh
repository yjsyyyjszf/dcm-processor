#!/bin/bash

rq-dashboard --redis-host "$REDIS_HOST" --redis-port "$REDIS_PORT" --redis-password "$REDIS_PSWD" -p 8080
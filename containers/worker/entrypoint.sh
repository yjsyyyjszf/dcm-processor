#!/bin/bash

export TZ=Europe/Berlin
export DEBIAN_FRONTEND=noninteractive
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

REQUIREMENTS="$MODULES/requirements.txt"
SLOGS="$LOGS/shell.txt"
PLOGS="$LOGS/pip.txt"
SCRIPT="$MODULES/script.sh"

alias pip='python -m pip'

if [ -f "$REQUIREMENTS" ]; then
    python -m pip install -r "$REQUIREMENTS"
fi

if [ -f "$SCRIPT" ]; then
    bash "$SCRIPT"
fi

when-changed "$REQUIREMENTS" -c python -m pip install -r %f >> $PLOGS &

when-changed "$SCRIPT" -c bash %f >> $SLOGS &

rq worker --path "$MODULES" -u "redis://:$REDIS_PSWD@$REDIS_HOST:$REDIS_PORT"  $JOBS
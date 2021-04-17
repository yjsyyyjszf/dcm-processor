#!/bin/bash

export TZ=Europe/Berlin
export DEBIAN_FRONTEND=noninteractive
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

REQUIREMENTS="$MODULES/*/requirements.txt"
SLOGS="$LOGS/shell.txt"
PLOGS="$LOGS/pip.txt"
SCRIPTS="$MODULES/*/script.sh"

alias pip='python -m pip'

for REQUIREMENT in $(ls $REQUIREMENTS)
do
  python -m pip install -r "$REQUIREMENT"
done

for SCRIPT in $(ls $SCRIPTS)
do
  bash "$SCRIPT"
done

when-changed "$REQUIREMENTS" -c python -m pip install -r %f >> $PLOGS &

when-changed "$SCRIPTS" -c bash %f >> $SLOGS &

rq worker --path "$MODULES" -u "redis://:$REDIS_PSWD@$REDIS_HOST:$REDIS_PORT"  $JOBS
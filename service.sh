#!/bin/bash

BASEDIR=./mapped_folders


usage()
{
  echo "Usage: $0 [-h] [action] [servicename] [ -p SERVICE_PATH ] [ -b BACKUP_PATH  ]"
  echo "actions: [install | remove | backup]"
  echo "-h      To show this help message"
  echo "-p      Path to the folder where the service data is. this is a directory with two sub-directories [registry and module]"
  echo "-b      Path to the folder where the service backup will be place. supported by [remove and backup] actions"
  exit 2
}

set_variable()
{
  local varname=$1
  shift
  if [ -z "${!varname}" ]; then
    eval "$varname=\"$@\""
  else
    echo "Error: $varname already set"
    usage
  fi
}

valid_action_type()
{
    case "$1" in
    "install"|"remove"|"backup")
        return 0;;
    *)
        echo "Action $1 is not supported"
        return 1;;
    esac
}


unset ACTION SERVICENAME SERVICEPATH BACKUPPATH

if ! valid_action_type "$1"; then
    usage
    exit 1
fi

ACTION=$1
SERVICENAME=$2
shift 2

[ -z "$SERVICENAME" ] && usage && exit 1

[[ $SERVICENAME == -* ]] && usage && exit 1


# Install
if [ $ACTION = "install" ]
then

  while getopts ':p:?h:' c; do
    case $c in
      p) set_variable SERVICEPATH $OPTARG ;;
      h|?) usage ;;
    esac
  done

  if [ -z "$SERVICEPATH" ]
  then
    read -p "Enter Service Path :" SERVICEPATH
  fi

  echo "copying module folder..."
  cp -r "$SERVICEPATH/module" "$BASEDIR/modules/$SERVICENAME"
  echo "copying registry folder..."
  cp -r "$SERVICEPATH/registry" "$BASEDIR/registry/$SERVICENAME"

fi



# Backup
if [ $ACTION = "backup" ]
then

  while getopts ':b:?h:' c; do
    case $c in
      b) set_variable BACKUPPATH $OPTARG ;;
      h|?) usage ;;
    esac
  done

  if [ -z "$BACKUPPATH" ]
  then
    read -p "Enter Backup Path :" SERVICEPATH
  fi

  mkdir -p "$BACKUPPATH/$SERVICENAME"
  echo "Copying registry entry"
  cp -r "$BASEDIR/registry/$SERVICENAME" "$BACKUPPATH/$SERVICENAME/registry"
  echo "Copying modules entry"
  cp -r "$BASEDIR/modules/$SERVICENAME" "$BACKUPPATH/$SERVICENAME/module"

fi




# Remove
if [ $ACTION = "remove" ]
then

  while getopts ':b:?h:' c; do
    case $c in
      b) set_variable BACKUPPATH $OPTARG ;;
      h|?) usage ;;
    esac
  done

  if [ -z "$BACKUPPATH" ]
  then
    echo "removing registry entry"
    rm -rf "$BASEDIR/registry/$SERVICENAME"
    echo "removing modules entry"
    rm -rf "$BASEDIR/modules/$SERVICENAME"
  else
    mkdir -p "$BACKUPPATH/$SERVICENAME"
    echo "Moving registry entry"
    mv "$BASEDIR/registry/$SERVICENAME" "$BACKUPPATH/$SERVICENAME/registry"
    echo "Moving modules entry"
    mv "$BASEDIR/modules/$SERVICENAME" "$BACKUPPATH/$SERVICENAME/module"
  fi

fi
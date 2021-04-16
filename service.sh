#!/bin/bash

BASEDIR=./mapped_folders

if [ $1 = "install" ]
then
  
  while getopts n:p: flag
  do
    case "${flag}" in
        n) servicename=${OPTARG};;
        p) servicepath=${OPTARG};;
    esac
  done

  if [ -z "$servicename" ]
  then
    read -p "Enter Service Name :" servicename
  fi

  if [ -z "$servicepath" ]
  then
    read -p "Enter Service Path :" servicepath
  fi
  
  cp -r "$servicepath/module" "$BASEDIR/modules/$servicename"
  cp -r "$servicepath/registry" "$BASEDIR/registry/$servicename"

fi
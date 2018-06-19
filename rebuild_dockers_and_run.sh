#!/bin/bash
./clean_dockers.sh
docker volume rm db_data
docker volume create --name db_data -d local
./gradle_build.sh
docker-compose up --build

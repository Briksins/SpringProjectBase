#!/bin/bash
docker build -t gradle-build . -f deployment/build/Dockerfile
cmd='docker run -it --rm -v gradle:/home/gradle/.gradle/ -v $(pwd):/opt/SpringProjectBase -e ACTION=build gradle-build'
echo "Executing:" $cmd
/bin/sh -c "$cmd"
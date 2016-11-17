#!/usr/bin/env bash

#port=$1
#host=":9999"

#docker-compose run -d -p $port$host tschm/ipy:v0.3

docker run -d -p 2019:9999 -v $(pwd)/books:/jupyter tschm/ipy:v0.3

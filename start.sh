#!/usr/bin/env bash

port=$1
host=":5000"

docker-compose run -d -p $port$host pytalk
google-chrome "http://localhost:$port/tree"



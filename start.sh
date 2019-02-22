#!/usr/bin/env bash
echo "http://localhost:8884"
docker-compose run -p "8884:8888" jupyter

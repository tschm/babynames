#!/usr/bin/env bash
docker build -t baby .
docker run --rm -p 8888:8888 baby

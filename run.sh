#!/usr/bin/env bash
chgrp -R 100 $(pwd)/books
docker build -t baby .
docker run -it -p "8888:8888" -v $(pwd)/books:/home/jovyan/work baby
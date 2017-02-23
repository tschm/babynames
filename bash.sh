#!/usr/bin/env bash

# unfortunately this doesn't really work on Windows as pwd is not available
docker run -it -v $(pwd)/books:/jupyter tschm/ipy:v0.5 /bin/bash
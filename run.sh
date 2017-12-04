#!/usr/bin/env bash

# (Empty) Folder with my local notebooks
FOLDER=/home/thomas/babynames/work/books2
echo $FOLDER

# All files in the folder will be promoted into group users
#sudo chgrp -R 100 $FOLDER

# This will be true also for all new files in the group
#sudo chmod -R 770 $FOLDER

docker run --rm -p 8888:8888 -v $FOLDER:/home/jovyan/work/books baby

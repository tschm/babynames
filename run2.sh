#!/usr/bin/env bash

# (Empty) Folder with my local notebooks
FOLDER=/home/thomas/babynames/work/books
echo $FOLDER

# All files in the folder will be promoted into group users
sudo chgrp -R 100 $FOLDER

# All files in this folder will be writeable by the group users
sudo chmod -R 770 $FOLDER

docker run --rm -p 8888:8888 -v $FOLDER:/home/jovyan/work/books tschm/babynames











#!/usr/bin/env bash

# (Empty) Folder with my local notebooks
FOLDER=$(pwd)/scripts
echo $FOLDER

USER=$(whoami)
echo $USER

# make sure that you are a member of the users group
# sudo usermod -a -G users $USER
# you have to logout and login again to make this really happen

# All files in the folder will be promoted into group users
#sudo chgrp -R 100 $FOLDER
chown -R $USER:users $FOLDER

# This will be true also for all new files in the group?
chmod -R 777 $FOLDER

docker run --rm -p 8888:8888 -v $FOLDER:/home/jovyan/work baby

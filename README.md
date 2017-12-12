This image is based on the standard-image jupyter/datascience-notebook:latest

Here are a few hints:



The local user should be a member of the group users
```
USER=$(whoami)
echo $USER

# make sure that you are a member of the users group
sudo usermod -a -G users $USER
```

You have to logout to make this happen...


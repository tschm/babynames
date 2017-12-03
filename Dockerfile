FROM jupyter/datascience-notebook:latest

# install other packages you may need, use pip or conda
ADD ./data /data

#USER root

USER root:100

CMD start-notebook.sh
### --NotebookApp.token=''

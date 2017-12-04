FROM jupyter/datascience-notebook:latest

# install other packages you may need, use pip or conda
ADD ./data /home/jovyan/work/data

USER root:100

CMD start-notebook.sh

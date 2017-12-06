FROM jupyter/datascience-notebook:latest

ADD ./data /home/jovyan/work/data
ADD ./config.json /home/jovyan/.jupyter/jupyter_notebook_config.json

USER root

# install cvxpy
RUN conda install -y -c cvxgrp cvxpy

CMD start-notebook.sh

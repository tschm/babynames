FROM jupyter/datascience-notebook:latest

RUN conda install -y -c cvxgrp cvxpy
RUN conda install -y -c conda-forge tensorflow

ADD ./data /home/jovyan/work/data
ADD ./config.json /home/jovyan/.jupyter/jupyter_notebook_config.json

USER root

CMD start-notebook.sh

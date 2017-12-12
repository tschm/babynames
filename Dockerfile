FROM jupyter/datascience-notebook:latest

RUN conda install -y numpy
RUN conda install -y -c cvxgrp cvxpy libgcc
RUN conda install -y -c conda-forge tensorflow

ADD ./config.json /home/jovyan/.jupyter/jupyter_notebook_config.json
ADD ./scripts /home/jovyan/work

USER root

CMD start-notebook.sh

# Set the base image to jupyter
FROM jupyter/base-notebook:1386e2046833 as jupyter

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

# copy the config.ini file
COPY /binder/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

RUN conda install -y -c conda-forge nomkl pandas cvxpy beakerx && \
    conda clean -y --all

COPY --chown=jovyan:100 ./work /home/jovyan/work
# Set the base image to jupyter
FROM jupyter/minimal-notebook:45b8529a6bfc

RUN conda config --env --add pinned_packages 'openjdk>8.0.121'
RUN conda install -y -c conda-forge pandas=0.24.1 beakerx=1.3.0 ipywidgets=7.4.2 matplotlib && conda clean -y --all

COPY ./books ${HOME}/work

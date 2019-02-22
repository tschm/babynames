# Set the base image to jupyter
FROM jupyter/minimal-notebook:45b8529a6bfc
RUN conda install -y -c conda-forge pandas=0.24.1 matplotlib scipy=1.2.1 && conda clean -y --all
COPY ./work ${HOME}/work

# Set the base image to jupyter
FROM lobnek/jupyter:v2.3

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

USER root
RUN conda install -y -c conda-forge matplotlib scipy=1.2.1 && conda clean -y --all
USER ${NB_USER}

COPY ./work /home/${NB_USER}/work

# Set the base image to jupyter
FROM lobnek/jupyter:v2.5

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

USER root
RUN conda install -y -c conda-forge scipy && conda clean -y --all
USER ${NB_USER}

COPY ./work /home/${NB_USER}/work

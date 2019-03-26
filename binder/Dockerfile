# Set the base image to jupyter
FROM lobnek/jupyter:v2.6

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# we need this for the entropy function
RUN pip install --no-cache-dir scipy

COPY ./work /home/${NB_USER}/work

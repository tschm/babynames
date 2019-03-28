# Set the base image to jupyter
FROM lobnek/jupyter:v2.8

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@lobnek.com"

# scipy is already in the image but nevertheless, let's install it
# we need this for the entropy function, do not install with conda...
# RUN pip install --no-cache-dir scipy

COPY --chown=beakerx:beakerx ./work /home/${NB_USER}/work

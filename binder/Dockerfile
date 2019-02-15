# Set the base image to beakerx
FROM beakerx/beakerx:1.3.0

USER root

RUN conda install -n beakerx -c conda-forge cvxpy=1.0.14 matplotlib


COPY ./books ${HOME}/books

# set the user back to NB_USER defined in Dockerfile for beakerx/beakerx
USER ${NB_USER}
# Set the base image to beakerx
FROM beakerx/beakerx:1.3.0

USER root

RUN conda install -n beakerx -c conda-forge cvxpy=1.0.14 matplotlib

# the password is geneva18
COPY jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

# set the user back to NB_USER defined in Dockerfile for beakerx/beakerx
USER $NB_USER
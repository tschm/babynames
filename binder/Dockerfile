# Set the base image to jupyter
FROM tschm/docker:release-0.4

# scipy is already in the image but nevertheless, let's install it
# we need this for the entropy function, do not install with conda...
# RUN pip install --no-cache-dir scipy

COPY --chown=jovyan:100 ./work ${WORK}

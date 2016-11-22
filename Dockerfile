## Set the base image to Ubuntu
FROM tschm/ipy:v0.5

RUN conda install -q -y seaborn


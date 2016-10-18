# Set the base image to Ubuntu
FROM continuumio/miniconda3

# File Author / Maintainer
MAINTAINER Thomas Schmelzer "thomas.schmelzer@gmail.com"

RUN conda install -q -y pandas=0.18.1 ipython-notebook=4.0.4 matplotlib

ADD . /babynames
WORKDIR /babynames

# create the default profile for ipython
RUN ipython profile create

EXPOSE 5000

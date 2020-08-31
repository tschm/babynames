#!make
PROJECT_VERSION := 2.0.2

SHELL := /bin/bash
IMAGE := tschm/babynames

.PHONY: help build jupyter tag #clean-notebooks


.DEFAULT: help

help:
	@echo "make build"
	@echo "       Build the docker image."
	@echo "make jupyter"
	@echo "       Start the Jupyter server."
	@echo "make tag"
	@echo "       Make a tag on Github."


build:
	docker-compose build jupyter

jupyter: build
	echo "http://localhost:8888"
	docker-compose up jupyter

jupyterlab: build
	echo "http://localhost:8888/lab"
	docker-compose up jupyter

tag:
	git tag -a ${PROJECT_VERSION} -m "new tag"
	git push --tags

#clean-notebooks:
#	docker-compose exec jupyter jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace /home/jovyan/work/**/*.ipynb

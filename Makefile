# "source" is a bash internal
SHELL := /bin/bash

# install the scripted folder
install:
	python add-scripted-to-path
	source ~/.bash_profile

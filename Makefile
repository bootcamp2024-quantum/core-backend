ifneq ("$(wildcard .env)","")
    include .env
    export $(shell sed 's/=.*//' .env)
else
endif

WORKDIR := $(shell pwd)
.ONESHELL:
.EXPORT_ALL_VARIABLES:
DOCKER_BUILDKIT=1


PORT?=8000


help: ## Display help message
	@echo "Please use \`make <target>' where <target> is one of"
	@perl -nle'print $& if m{^[\.a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

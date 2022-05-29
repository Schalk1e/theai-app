-include .config/env

az-login:
	az login

az-build:
	az acr build \
	--registry theai-app \
	--subscription theai-app \
	--image theai-app .

build-local:
	docker build \
	-t theai-app .

run-local:
	docker run --rm \
	-e THEAI_APP_STORAGE_CONNECTION_STRING=$(THEAI_APP_STORAGE_CONNECTION_STRING) \
	-e PORT=$(PORT) \
	-e SECRET_KEY=$(SECRET_KEY) \
	-p 0.0.0.0:$(PORT):$(PORT) \
	-v $(shell pwd):/usr/src/app \
	-it theai-app

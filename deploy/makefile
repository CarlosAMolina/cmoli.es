ROOT_PATHNAME=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SCRIPT_CONVERT_MD_TO_HTML_PATHNAME=$(ROOT_PATHNAME)/convert-md-to-html-for-files
SCRIPT_OPEN_HTML_PATHNAME=$(ROOT_PATHNAME)/open-html
SCRIPT_SEND_FILES_TO_VPS_PATHNAME=$(ROOT_PATHNAME)/send-files-to-vps
DOCKER_NGINX_IMAGE_NAME=nginx:latest
DOCKER_PANDOC_IMAGE_NAME=pandoc/minimal:2.17-alpine
DOCKER_PYTHON_IMAGE_NAME=python:3.8.15-alpine3.16
DOCKER_VOLUME_NAME_NGINX_LOGS=nginx-logs
DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT=nginx-web-content
DOCKER_VOLUME_NAME_PANDOC=pandoc
URL_NGINX_LOCALHOST=http://localhost:8080
VPS_SRC_OUTPUT_PATHNAME=/var/www/cmoli.es/html

activate-docker-if-not-active:
	/bin/bash activate-docker-service-if-not-active

create-web-content:
	git pull origin $(shell git branch --show-current)
	/bin/bash remove-volumes \
		$(DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT) \
		$(DOCKER_VOLUME_NAME_PANDOC)
	/bin/bash $(SCRIPT_CONVERT_MD_TO_HTML_PATHNAME) \
		$(DOCKER_PANDOC_IMAGE_NAME) \
		$(DOCKER_PYTHON_IMAGE_NAME) \
		$(DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT) \
		$(DOCKER_VOLUME_NAME_PANDOC)

create-web-server:
	make -f makefile-nginx \
		run \
		DOCKER_IMAGE_NAME=$(DOCKER_NGINX_IMAGE_NAME) \
		DOCKER_VOLUME_NGINX_WEB_CONTENT=$(DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT) \
		DOCKER_VOLUME_NGINX_LOGS=$(DOCKER_VOLUME_NAME_NGINX_LOGS) \
		URL_NGINX_LOCALHOST=$(URL_NGINX_LOCALHOST)

show-web:
	/bin/bash $(SCRIPT_OPEN_HTML_PATHNAME) \
		$(URL_NGINX_LOCALHOST) \
		$(DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT)

show-logs:
	make -f makefile-nginx \
		logs \
		DOCKER_VOLUME_NGINX_LOGS=$(DOCKER_VOLUME_NAME_NGINX_LOGS)

deploy-send-files-to-vps:
	/bin/bash $(SCRIPT_SEND_FILES_TO_VPS_PATHNAME) \
		$(DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT) \
		$(VPS_SRC_OUTPUT_PATHNAME)

stop-containers:
	make -f makefile-nginx \
	    stop-if-running

test: activate-docker-if-not-active stop-containers create-web-content create-web-server show-web

deploy: activate-docker-if-not-active stop-containers create-web-content deploy-send-files-to-vps

export-pandoc-template-html:
	# https://pandoc.org/MANUAL.html#option--print-default-template
	pandoc -D html > /tmp/template-default.html

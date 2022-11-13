ROOT_PATHNAME:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SCRIPT_CONVERT_MD_TO_HTML_PATHNAME:=$(ROOT_PATHNAME)/convert-md-to-html-for-files
SCRIPT_OPEN_HTML_PATHNAME:=$(ROOT_PATHNAME)/open-html
SCRIPT_SEND_FILES_TO_VPS_PATHNAME:=$(ROOT_PATHNAME)/send-files-to-vps
DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT:=nginx-web-content
DOCKER_VOLUME_NAME_PANDOC:=pandoc
VPS_SRC_OUTPUT_PATHNAME:=/var/www/cmoli.es/html

create-web:
	docker volume rm $(DOCKER_VOLUME_NAME_PANDOC)
	docker volume rm $(DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT)
	/bin/bash $(SCRIPT_CONVERT_MD_TO_HTML_PATHNAME) $(DOCKER_VOLUME_NAME_PANDOC)

show-web:
	/bin/bash $(SCRIPT_OPEN_HTML_PATHNAME) \
		$(DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT)

deploy-send-files-to-vps:
	/bin/bash $(SCRIPT_SEND_FILES_TO_VPS_PATHNAME) \
		$(DOCKER_VOLUME_NAME_NGINX_WEB_CONTENT) \
		$(VPS_SRC_OUTPUT_PATHNAME)

test: create-web show-web

deploy: create-web deploy-send-files-to-vps

export-pandoc-template-html:
	# https://pandoc.org/MANUAL.html#option--print-default-template
	pandoc -D html > /tmp/template-default.html

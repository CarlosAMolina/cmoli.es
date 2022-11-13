ROOT_PATHNAME:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
# TODO OUTPUT_PATHNAME:=/tmp/cmoli.es
# TODO SRC_OUTPUT_PATHNAME:=$(OUTPUT_PATHNAME)/html
# TODO VPS_SRC_OUTPUT_PATHNAME:=/var/www/cmoli.es/html
SCRIPT_CONVERT_MD_TO_HTML_PATHNAME:=$(ROOT_PATHNAME)/convert-md-to-html-for-files
SCRIPT_OPEN_HTML_PATHNAME:=$(ROOT_PATHNAME)/open-html
VOLUME_NAME_NGINX_WEB_CONTENT:=nginx-web-content
VOLUME_NAME_PANDOC:=pandoc

create-web:
	docker volume rm $(VOLUME_NAME_PANDOC)
	docker volume rm $(VOLUME_NAME_NGINX_WEB_CONTENT)
	/bin/bash $(SCRIPT_CONVERT_MD_TO_HTML_PATHNAME)

show-web:
	/bin/bash $(SCRIPT_OPEN_HTML_PATHNAME)

#TODO send-files:
#TODO 	scp -P $(VPS_DEV_PORT) -r $(SRC_OUTPUT_PATHNAME)/* $(VPS_DEV_USER)@$(VPS_DEV_IP):$(VPS_SRC_OUTPUT_PATHNAME)/

test: create-web show-web

deploy: create-web send-files

export-pandoc-template-html:
	# https://pandoc.org/MANUAL.html#option--print-default-template
	pandoc -D html > /tmp/template-default.html

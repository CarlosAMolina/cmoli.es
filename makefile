ROOT_PATHNAME:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
OUTPUT_PATHNAME:=/tmp/cmoli.es
SRC_OUTPUT_PATHNAME:=$(OUTPUT_PATHNAME)/html
PANDOC_CONFIG_PATHNAME:=$(ROOT_PATHNAME)/pandoc-config
PANDOC_METADATA_INPUT_PATHNAME:=$(PANDOC_CONFIG_PATHNAME)/metadata.yml
PANDOC_TEMPLATE_INPUT_PATHNAME:=$(PANDOC_CONFIG_PATHNAME)/template.html
SCRIPT_CONVERT_MD_TO_HTML_PATHNAME:=$(OUTPUT_PATHNAME)/run-md-to-html
VPS_SRC_OUTPUT_PATHNAME:=/var/www/cmoli.es/html

create-web:
	rm -rf $(OUTPUT_PATHNAME)
	mkdir $(OUTPUT_PATHNAME)
	mkdir $(SRC_OUTPUT_PATHNAME)
	cp -r src/* $(SRC_OUTPUT_PATHNAME)
	python md-to-html/src/main.py \
		$(SRC_OUTPUT_PATHNAME)/blog.css \
		$(PANDOC_METADATA_INPUT_PATHNAME) \
		$(PANDOC_TEMPLATE_INPUT_PATHNAME) \
		$(SRC_OUTPUT_PATHNAME) \
		$(SCRIPT_CONVERT_MD_TO_HTML_PATHNAME)
	chmod +x $(SCRIPT_CONVERT_MD_TO_HTML_PATHNAME)
	/bin/bash $(SCRIPT_CONVERT_MD_TO_HTML_PATHNAME)

send-files:
	scp -P $(VPS_DEV_PORT) -r $(SRC_OUTPUT_PATHNAME)/* $(VPS_DEV_USER)@$(VPS_DEV_IP):$(VPS_SRC_OUTPUT_PATHNAME)/

open-html:
	firefox $(SRC_OUTPUT_PATHNAME)/index.html

test: create-web open-html

deploy: create-web send-files

export-template-html:
	# https://pandoc.org/MANUAL.html#option--print-default-template
	pandoc -D html > /tmp/template-default.html

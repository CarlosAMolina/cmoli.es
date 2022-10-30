SRC_OUTPUT_VPS_PATHNAME:=/var/www/cmoli.es/html
OUTPUT_LOCAL_PATHNAME:=/tmp/cmoli.es
SRC_OUTPUT_LOCAL_PATHNAME:=$(OUTPUT_LOCAL_PATHNAME)/html
PANDOC_TEMPLATE_INPUT_LOCAL_PATHNAME:=pandoc-config/template.html
PANDOC_METADATA_INPUT_LOCAL_PATHNAME:=pandoc-config/metadata.yml
SCRIPT_NAME_CONVERT_MD_TO_HTML=run-md-to-html

create-web:
	rm -rf $(OUTPUT_LOCAL_PATHNAME)
	mkdir $(OUTPUT_LOCAL_PATHNAME)
	mkdir $(SRC_OUTPUT_LOCAL_PATHNAME)
	cp -r src/* $(SRC_OUTPUT_LOCAL_PATHNAME)
	python md-to-html/src/main.py $(SRC_OUTPUT_LOCAL_PATHNAME)/blog.css $(PANDOC_METADATA_INPUT_LOCAL_PATHNAME) $(PANDOC_TEMPLATE_INPUT_LOCAL_PATHNAME) $(SRC_OUTPUT_LOCAL_PATHNAME) $(SCRIPT_NAME_CONVERT_MD_TO_HTML)
	chmod +x $(SCRIPT_NAME_CONVERT_MD_TO_HTML)
	./$(SCRIPT_NAME_CONVERT_MD_TO_HTML)
	rm $(SCRIPT_NAME_CONVERT_MD_TO_HTML)

send-files:
	scp -P $(VPS_DEV_PORT) -r $(SRC_OUTPUT_LOCAL_PATHNAME)/* $(VPS_DEV_USER)@$(VPS_DEV_IP):$(SRC_OUTPUT_VPS_PATHNAME)/

open-html:
	firefox $(SRC_OUTPUT_LOCAL_PATHNAME)/index.html

test: create-web open-html

deploy: create-web send-files

export-template-html:
	# https://pandoc.org/MANUAL.html#option--print-default-template
	pandoc -D html > /tmp/template-default.html

SRC_OUTPUT_VPS_PATHNAME:=/var/www/cmoli.es/html
OUTPUT_LOCAL_PATHNAME:=/tmp/cmoli.es
SRC_OUTPUT_LOCAL_PATHNAME:=$(OUTPUT_LOCAL_PATHNAME)/html
BLOG_SRC_OUTPUT_LOCAL_PATHNAME:=$(SRC_OUTPUT_LOCAL_PATHNAME)/blog
CSS_BLOG_SRC_OUTPUT_LOCAL_PATHNAME:=../blog.css
WIKI_SRC_OUTPUT_LOCAL_PATHNAME:=$(SRC_OUTPUT_LOCAL_PATHNAME)/wiki
PANDOC_TEMPLATE_INPUT_LOCAL_PATHNAME:=pandoc-config/template.html
PANDOC_METADATA_INPUT_LOCAL_PATHNAME:=pandoc-config/metadata.yml

create-web:
	rm -rf $(OUTPUT_LOCAL_PATHNAME)
	mkdir $(OUTPUT_LOCAL_PATHNAME)
	mkdir $(SRC_OUTPUT_LOCAL_PATHNAME)
	cp -r src/* $(SRC_OUTPUT_LOCAL_PATHNAME)
	./convert-md-to-html $(BLOG_SRC_OUTPUT_LOCAL_PATHNAME)/2021-05-15-leer-periodicos-online-sin-iniciar-sesion.md $(BLOG_SRC_OUTPUT_LOCAL_PATHNAME)/2021-05-15-leer-periodicos-online-sin-iniciar-sesion.html $(CSS_BLOG_SRC_OUTPUT_LOCAL_PATHNAME) $(PANDOC_TEMPLATE_INPUT_LOCAL_PATHNAME) $(PANDOC_METADATA_INPUT_LOCAL_PATHNAME)
	./convert-md-to-html $(BLOG_SRC_OUTPUT_LOCAL_PATHNAME)/2021-09-12-utilizar-protonmail-con-tor-y-no-con-protonvpn.md $(BLOG_SRC_OUTPUT_LOCAL_PATHNAME)/2021-09-12-utilizar-protonmail-con-tor-y-no-con-protonvpn.html $(CSS_BLOG_SRC_OUTPUT_LOCAL_PATHNAME) $(PANDOC_TEMPLATE_INPUT_LOCAL_PATHNAME) $(PANDOC_METADATA_INPUT_LOCAL_PATHNAME)
	./convert-md-to-html $(WIKI_SRC_OUTPUT_LOCAL_PATHNAME)/ssh.md $(WIKI_SRC_OUTPUT_LOCAL_PATHNAME)/ssh.html $(CSS_BLOG_SRC_OUTPUT_LOCAL_PATHNAME) $(PANDOC_TEMPLATE_INPUT_LOCAL_PATHNAME) $(PANDOC_METADATA_INPUT_LOCAL_PATHNAME)

send-files:
	scp -P $(VPS_DEV_PORT) -r $(SRC_OUTPUT_LOCAL_PATHNAME)/* $(VPS_DEV_USER)@$(VPS_DEV_IP):$(SRC_OUTPUT_VPS_PATHNAME)/

open-html:
	firefox $(SRC_OUTPUT_LOCAL_PATHNAME)/index.html

test: create-web open-html

deploy: create-web send-files

export-template-html:
	# https://pandoc.org/MANUAL.html#option--print-default-template
	pandoc -D html > /tmp/template-default.html

DESTINATION_PATHNAME:=/tmp/web
HTML_DESTINATION_PATHNAME:=$(DESTINATION_PATHNAME)/html
HTML_BLOG_DESTINATION_PATHNAME:=$(HTML_DESTINATION_PATHNAME)/blog
HTML_BLOG_CSS_DESTINATION_PATHNAME:=$(HTML_DESTINATION_PATHNAME)/blog.css
HTML_WIKI_DESTINATION_PATHNAME:=$(HTML_DESTINATION_PATHNAME)/wiki
PANDOC_CONFIG_DESTINATION_PATHNAME:=$(DESTINATION_PATHNAME)/pandoc-config
PANDOC_TEMPLATE_DESTINATION_PATHNAME:=$(PANDOC_CONFIG_DESTINATION_PATHNAME)/template.html
PANDOC_METADATA_DESTINATION_PATHNAME:=$(PANDOC_CONFIG_DESTINATION_PATHNAME)/metadata.yml

create-web:
	rm -rf $(DESTINATION_PATHNAME)
	mkdir $(DESTINATION_PATHNAME)
	mkdir $(HTML_DESTINATION_PATHNAME)
	mkdir $(HTML_BLOG_DESTINATION_PATHNAME)
	mkdir $(HTML_WIKI_DESTINATION_PATHNAME)
	mkdir $(PANDOC_CONFIG_DESTINATION_PATHNAME)
	cp src/index.html $(HTML_DESTINATION_PATHNAME)
	cp src/index.css $(HTML_DESTINATION_PATHNAME)
	cp src/avatar.png $(HTML_DESTINATION_PATHNAME)
	cp src/blog/blog.css $(HTML_BLOG_CSS_DESTINATION_PATHNAME)
	cp -r src/felices-fiestas $(HTML_DESTINATION_PATHNAME)
	cp pandoc-config/* $(PANDOC_CONFIG_DESTINATION_PATHNAME)/
	./convert-md-to-html src/blog/2021-05-15-leer-periodicos-online-sin-iniciar-sesion.md $(HTML_BLOG_DESTINATION_PATHNAME)/2021-05-15-leer-periodicos-online-sin-iniciar-sesion.html $(HTML_BLOG_CSS_DESTINATION_PATHNAME) $(PANDOC_TEMPLATE_DESTINATION_PATHNAME) $(PANDOC_METADATA_DESTINATION_PATHNAME)
	./convert-md-to-html src/blog/2021-09-12-utilizar-protonmail-con-tor-y-no-con-protonvpn.md $(HTML_BLOG_DESTINATION_PATHNAME)/2021-09-12-utilizar-protonmail-con-tor-y-no-con-protonvpn.html $(HTML_BLOG_CSS_DESTINATION_PATHNAME) $(PANDOC_TEMPLATE_DESTINATION_PATHNAME) $(PANDOC_METADATA_DESTINATION_PATHNAME)
	./convert-md-to-html src/wiki/ssh.md $(HTML_WIKI_DESTINATION_PATHNAME)/ssh.html $(HTML_BLOG_CSS_DESTINATION_PATHNAME) $(PANDOC_TEMPLATE_DESTINATION_PATHNAME) $(PANDOC_METADATA_DESTINATION_PATHNAME)

open-html:
	firefox $(HTML_DESTINATION_PATHNAME)/index.html

all: create-web open-html

export-template-html:
	# https://pandoc.org/MANUAL.html#option--print-default-template
	pandoc -D html > /tmp/template-default.html

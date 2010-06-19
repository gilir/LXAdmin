NULL=

SUBDIRS=

fontconfigdir = $(prefix)/bin

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 lxfontconfig.py "$(DESTDIR)$(bindir)/lxfontconfig"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/lxfontconfig

EXTRA_DIST =  \
    lxfontconfig.py \
	$(NULL)

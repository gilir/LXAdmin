NULL=

SUBDIRS=

fontconfigdir = $(prefix)/bin

DISTCLEANFILES = fontconfig.py

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 fontconfig.py "$(DESTDIR)$(bindir)/fontconfig"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/fontconfig

EXTRA_DIST =  \
    fontconfig.py \
	$(NULL)

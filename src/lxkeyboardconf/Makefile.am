NULL=

SUBDIRS=

keyboardconfdir = $(prefix)/bin

DISTCLEANFILES = keyboardconf.py

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 keyboardconf.py "$(DESTDIR)$(bindir)/keyboardconf"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/keyboardconf

EXTRA_DIST =  \
    keyboardconf.py \
	$(NULL)

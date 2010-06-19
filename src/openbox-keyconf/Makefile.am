NULL=

SUBDIRS=

openboxkeyconfdir = $(prefix)/bin

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 openbox-keyconf.py "$(DESTDIR)$(bindir)/openbox-keyconf"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/openbox-keyconf

EXTRA_DIST =  \
    openbox-keyconf.py \
	$(NULL)

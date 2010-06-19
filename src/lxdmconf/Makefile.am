NULL=

SUBDIRS=

lxdmconfdir = $(prefix)/bin

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 lxdmconf.py "$(DESTDIR)$(bindir)/lxdmconf"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/lxdmconf

EXTRA_DIST =  \
    lxdmconf.py \
	$(NULL)

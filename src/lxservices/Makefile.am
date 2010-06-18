NULL=

SUBDIRS=

lxservicesdir = $(prefix)/bin

DISTCLEANFILES = lxservices.py

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 lxservices.py "$(DESTDIR)$(bindir)/lxservices"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/lxservices

EXTRA_DIST =  \
    lxservices.py \
	$(NULL)

NULL=

SUBDIRS=

servicesdir = $(prefix)/bin

DISTCLEANFILES = services.py

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 services.py "$(DESTDIR)$(bindir)/services"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/services

EXTRA_DIST =  \
    services.py \
	$(NULL)

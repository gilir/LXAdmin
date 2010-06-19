NULL=

SUBDIRS=

lxccdir = $(prefix)/bin

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 lxcc.py "$(DESTDIR)$(bindir)/lxcc"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/lxcc

EXTRA_DIST =  \
    lxcc.py \
	$(NULL)

NULL=

SUBDIRS=

lxscreenshotdir = $(prefix)/bin

DISTCLEANFILES = lxscreenshot.py

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 lxscreenshot.py "$(DESTDIR)$(bindir)/lxscreenshot"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/lxscreenshot

EXTRA_DIST =  \
	lxscreenshot.py \
	$(NULL)

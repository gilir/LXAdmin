NULL=

SUBDIRS=

screenshotdir = $(prefix)/bin

DISTCLEANFILES = screenshot.py

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 screenshot.py "$(DESTDIR)$(bindir)/screenshot"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/screenshot

EXTRA_DIST =  \
	screenshot.py \
	$(NULL)

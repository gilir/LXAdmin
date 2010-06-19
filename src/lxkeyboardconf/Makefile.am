NULL=

SUBDIRS=

lxkeyboardconfdir = $(prefix)/bin

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 lxkeyboardconf.py "$(DESTDIR)$(bindir)/lxkeyboardconf"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/lxkeyboardconf

EXTRA_DIST =  \
    lxkeyboardconf.py \
	$(NULL)

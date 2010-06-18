NULL=

SUBDIRS=

lxproxydir = $(prefix)/bin

lxproxymoduledir = $(pkgdatadir)
lxproxymodule_DATA =	\
	__init__.py	\
    AboutLxproxyDialog.py \
    lxproxyconfig.py \
    PreferencesLxproxyDialog.py \
	$(NULL)

DISTCLEANFILES = lxproxy.py

install-exec-local:
	test -e "$(DESTDIR)$(bindir)" || mkdir -p "$(DESTDIR)$(bindir)"
	$(INSTALL) -m 755 lxproxy.py "$(DESTDIR)$(bindir)/lxproxy"

uninstall-local:
	rm -f $(DESTDIR)$(bindir)/lxproxy

EXTRA_DIST =  \
    __init__.py.in \
    lxproxy.py \
    $(lxproxymodule_DATA) \
	$(NULL)

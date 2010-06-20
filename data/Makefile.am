NULL=

SUBDIRS= media

desktopdir=$(datadir)/applications
desktop_in_files = \
	$(wildcard *.desktop.in) \
	$(NULL)
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

CLEANFILES = \
	$(wildcard *.desktop)

DISTCLEANFILES = \
	$(CLEANFILES)

EXTRA_DIST= \
	$(desktop_DATA) \
	$(NULL)

NULL=

SUBDIRS= ui media

desktopdir=$(datadir)/applications
desktop_in_files = \
	fontconfig.desktop.in \
	keyboard-setup.desktop.in \
	lxcc.desktop.in \
	lxdmconf.desktop.in \
	lxproxy.desktop.in \
	openbox-keyconf.desktop.in \
	screenshot.py.desktop.in \
	services.py.desktop.in \
	$(NULL)
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

EXTRA_DIST= \
	$(desktop_DATA) \
	$(NULL)

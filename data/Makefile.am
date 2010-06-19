NULL=

SUBDIRS= media

desktopdir=$(datadir)/applications
desktop_in_files = \
	lxcc.desktop.in \
	lxdmconf.desktop.in \
	lxfontconfig.desktop.in \
	lxkeyboard-setup.desktop.in \
	lxproxy.desktop.in \
	lxscreenshot.desktop.in \
	lxservices.desktop.in \
	openbox-keyconf.desktop.in \
	$(NULL)
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

EXTRA_DIST= \
	$(desktop_DATA) \
	$(NULL)

NULL=

# GtkBuilder UI definition files
uidir=$(datadir)/lxproxy/ui
ui_DATA= \
	AboutLxproxyDialog.ui \
	LxproxyWindow.ui \
	PreferencesLxproxyDialog.ui \
	$(NULL)

xmldir=$(datadir)/lxproxy/ui
xml_DATA= \
	about_lxproxy_dialog.xml \
	lxproxy_window.xml \
	preferences_lxproxy_dialog.xml

CLEANFILES = \
	$(ui_DATA) \
	$(xml_DATA) \
	$(NULL)

# Purge GtkBuilder UI files
# %.ui: %.glade
#	cp $< $@
#	$(top_srcdir)/src/xml-purge $@

EXTRA_DIST= \
	$(ui_DATA) \
	$(xml_DATA) \
	$(NULL)

NULL=

# GtkBuilder UI definition files
uidir=$(datadir)/lxproxy/ui
ui_in_files= \
	AboutLxproxyDialog.ui \
	LxproxyWindow.ui \
	PreferencesLxproxyDialog.ui
	$(NULL)

ui_DATA = $(ui_in_files)

CLEANFILES = \
	$(ui_DATA) \
	$(NULL)

# Purge GtkBuilder UI files
# %.ui: %.glade
#	cp $< $@
#	$(top_srcdir)/src/xml-purge $@

EXTRA_DIST= \
	$(ui_DATA) \
	$(NULL)

NULL=

SUBDIRS= common lxcc lxdmconf lxfontconfig lxkeyboardconf lxproxy lxscreenshot lxservices openbox-keyconf

AM_CPPFLAGS = \
	-I$(srcdir) \
	-DPACKAGE_DATA_DIR=\""$(datadir)/lxadmin"\" \
	-DPACKAGE_UI_DIR=\""$(datadir)/lxadmin/ui"\" \
	-DPACKAGE_LOCALE_DIR=\""$(prefix)/$(DATADIRNAME)/locale"\" \
	$(NULL)

# Little program to optimize size of xml files
noinst_PROGRAMS=xml-purge
xml_purge_SOURCES=$(top_srcdir)/src/xml-purge.c
xml_purge_CFLAGS=$(GTK_CFLAGS)
xml_purge_LDADD=$(GTK_LIBS)

NULL=

SUBDIRS=

bin_SCRIPTS = lxproxy.py

lxproxydir = $(prefix)/bin

lxproxymoduledir = $(pythondir)/lxadmin
lxproxymodule_PYTHON =	\
	__init__.py	\
    AboutLxproxyDialog.py \
    lxproxyconfig.py \
    PreferencesLxproxyDialog.py \
	$(NULL)

DISTCLEANFILES = $(bin_SCRIPTS)         

EXTRA_DIST =  \
    __init__.py.in \
    $(bin_SCRIPTS) \
    $(lxproxy_PYTHON) \
	$(NULL)

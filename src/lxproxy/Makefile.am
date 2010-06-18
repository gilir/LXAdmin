NULL=

SUBDIRS=

bin_SCRIPTS = lxproxy.py

lxproxydir = $(prefix)/bin

lxproxy_moduledir = $(pyexecdir)/lxadmin
lxproxy_module_PYTHON =	\
	__init__.py	\
    AboutLxproxyDialog.py \
    lxproxyconfig.py \
    PreferencesLxproxyDialog.py \
	$(NULL)

EXTRA_DIST = __init__.py.in

DISTCLEANFILES = $(bin_SCRIPTS)         

EXTRA_DIST =  \
    $(bin_SCRIPTS) \
    $(lxproxy_PYTHON) \
	$(NULL)

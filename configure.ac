#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

prog_name = lxadmin

AC_PREREQ([2.63])
AC_INIT([lxadmin], [0.0.1], [https://launchpad.net/lxadmin])
AM_INIT_AUTOMAKE([-Wall -Werror foreign])
AC_CONFIG_MACRO_DIR([m4])
AC_SUBST(ACLOCAL_AMFLAGS, "$ACLOCAL_FLAGS -I m4")

AC_CONFIG_HEADERS([config.h])

# Checks for programs.
AC_PROG_CC
# AM_PROG_LIBTOOL

# Checks for libraries.

# Checks for header files.
AC_HEADER_STDC

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

# intltool
IT_PROG_INTLTOOL([0.40.0])

# Python support
AM_PATH_PYTHON([2.4])

# PKG_CHECK_MODULES(XLIB, "x11")
# AC_SUBST(XLIB_CFLAGS)
# AC_SUBST(XLIB_LIBS)

#Support for xml-purge.c
pkg_modules="gtk+-2.0 >= 2.12.0"
PKG_CHECK_MODULES(GTK, [$pkg_modules])
AC_SUBST(GTK_CFLAGS)
AC_SUBST(GTK_LIBS)

# gio_modules="gthread-2.0 gio-unix-2.0 glib-2.0 >= 2.18.0"
# PKG_CHECK_MODULES(GIO, [$gio_modules])
# AC_SUBST(GIO_CFLAGS)
# AC_SUBST(GIO_LIBS)

# menu_modules="libmenu-cache >= 0.3.2"
# PKG_CHECK_MODULES(MENU_CACHE, [$menu_modules])
# AC_SUBST(MENU_CACHE_CFLAGS)
# AC_SUBST(MENU_CACHE_LIBS)

AC_ARG_ENABLE(debug,
	[AC_HELP_STRING([--enable-debug],
		[build libfm with debug support @<:@default=no@:>@])],
	[enable_debug="${enableval}"],
	[enable_debug=no]
)
if test "$enable_debug" = "yes"; then
    # turn on debug and disable optimization
    CPPFLAGS="$CPPFLAGS -DG_ENABLE_DEBUG -O0 -g"
else
    # turn off glib debug checks
    CPPFLAGS="$CPPFLAGS -DG_DISABLE_ASSERT -DG_DISABLE_CHECKS -DG_DISABLE_CAST_CHECKS"
fi

# Generate po/LINGUAS on the fly rather than relying on translators
# to maintain it manually. This also overcome the problem that Transifex
# cannot add a language to po/LINGUAS if a new po file is submitted.
rm -f $srcdir/po/LINGUAS
for po_file in `ls $srcdir/po/*.po | sort`;
do
    lang=`echo "$po_file" | sed "s|.*/po/\(.*\)\.po|\1|g"`
    echo $lang >> $srcdir/po/LINGUAS
done

GETTEXT_PACKAGE=lxadmin
AC_SUBST(GETTEXT_PACKAGE)
AM_GLIB_GNU_GETTEXT
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [Gettext package.])

# Add system directory for defs.in

AC_SUBST(VERSION)
AC_SUBST(PACKAGE)

AS_AC_EXPAND(PYTHONDIR, $pythondir)
AS_AC_EXPAND(BINDIR, $bindir)
AS_AC_EXPAND(LOCALEDIR, $datarootdir/locale)
AS_AC_EXPAND(PKGDATADIR, $datarootdir/$PACKAGE)
AS_AC_EXPAND(DATADIR, $datarootdir/$PACKAGE)
AS_AC_EXPAND(DESKTOPFILEDIR, $datarootdir/applications)

AC_CONFIG_FILES([
    Makefile
    data/Makefile
    data/media/Makefile
    po/Makefile.in
    src/Makefile
    src/common/defs.py
    src/common/Makefile
    src/lxcc/Makefile
    src/lxdmconf/Makefile
    src/lxfontconfig/Makefile
    src/lxkeyboardconf/Makefile
    src/lxproxy/Makefile
    src/lxscreenshot/Makefile
    src/lxservices/Makefile
    src/openbox-keyconf/Makefile
])

AC_OUTPUT

if test x"$sysconfdir" != x'/etc'; then
    echo
    echo
    echo 'Error: sysconfdir is not /etc.'
    echo 'Please consider passing --sysconfdir=/etc to configure.';
    echo 'Otherwise default config files will be installed to wrong place.'
    echo
    echo
else
    echo
    echo lxadmin....................... : Version $VERSION
    echo
    echo Enable debug....................: "$enable_debug"
    echo Prefix..........................: $prefix
    echo
    echo The binary will be installed in $prefix/bin
    echo
    echo http://lxde.org/
    echo
    echo "Ready to make lxadmin. Type 'make' to continue."
    echo
fi

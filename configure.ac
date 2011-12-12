AC_PREREQ([2.63])
AC_INIT([bareftp], [0.3.90])

AC_CONFIG_MACRO_DIR([m4])

AM_PROG_LIBTOOL

AM_INIT_AUTOMAKE([1.11 -Wno-portability])

AC_SUBST(VERSION)

AM_PATH_GLIB_2_0(2.27.5,,,gobject)
if test "$GLIB_LIBS" = ""; then
   AC_MSG_ERROR(GLIB 2.27.5 or later is required to build libcaribou)
fi

dnl == check for python ==
AM_PATH_PYTHON(2.7)

# gettext
BAREFTP_CONFIGURE_I18N($PACKAGE)

BAREFTP_EXPAND_DATADIR

dnl == Library dependencies ==
PYGOBJECT_REQUIRED=2.90.3
GTK_REQUIRED=3.0.0
GDK_REQUIRED=3.0.0

PKG_CHECK_MODULES(CARIBOU, [
  pygobject-3.0 >= $PYGOBJECT_REQUIRED,
  gtk+-3.0      >= $GTK_REQUIRED
  ])

AC_SUBST(BAREFTP_CFLAGS)
AC_SUBST(BAREFTP_LIBS)

dnl == i18n ==
GETTEXT_PACKAGE=bareftp
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [The gettext package])
AM_GLIB_GNU_GETTEXT

dnl == intltool check ==
IT_PROG_INTLTOOL([0.35.0])

dnl == GObject introspection ==
GOBJECT_INTROSPECTION_REQUIRE([0.10.7])

dnl == generate makefiles ==
AC_OUTPUT([
Makefile
po/Makefile.in
bareftp/Makefile
bareftp/i18n.py
bareftp/version.py
])




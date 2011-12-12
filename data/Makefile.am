SUBDIRS = \
	icon-theme

desktopdir = $(datadir)/applications
desktop_in_files=bareftp.desktop.in.in
desktop_DATA=$(desktop_in_files:.desktop.in.in=.desktop)

%.desktop.in: %.desktop.in.in
	sed -e "s/\@VERSION\@/$(VERSION)/" < $< > $@ 

@INTLTOOL_DESKTOP_RULE@ 

EXTRA_DIST = \
	bareftp.1 \
	$(desktop_in_files)

man_MANS = \
	bareftp.1

MAINTAINERCLEANFILES = \
	Makefile.in

DISTCLEANFILES = \
	$(desktop_DATA)

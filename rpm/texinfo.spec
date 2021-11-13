Summary: Tools needed to create Texinfo format documentation files
Name: texinfo
Version: 6.7
Release: 1
License: GPLv3+
Url: http://www.gnu.org/software/texinfo/
Source0: %{name}-%{version}.tar.gz
Source1: info-dir
Patch0: texinfo-4.12-zlib.patch
Patch1: texinfo-disable-tex.patch
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: help2man
BuildRequires: libtool
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(ncurses)

%global __provides_exclude ^perl\\(.*Texinfo.*\\)$
%global __requires_exclude ^perl\\(.*Texinfo.*\\)$
%global __provides_exclude %__provides_exclude|^perl\\(.*gettext_xs.*\\)$
%global __requires_exclude %__requires_exclude|^perl\\(.*gettext_xs.*\\)$

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description doc
Man and info pages for %{name}.

%package -n info
Summary: A stand-alone TTY-based reader for GNU texinfo documentation

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.

%package -n info-doc
Summary:   Documentation for info
Requires:  info = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description -n info-doc
Man and info pages for info.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
./autogen.sh
%configure --disable-perl-xs
%make_build

%install
mkdir -p ${RPM_BUILD_ROOT}/sbin

%make_install

install -p -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_infodir}/dir
mv $RPM_BUILD_ROOT%{_bindir}/install-info $RPM_BUILD_ROOT/sbin

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m0644 -t $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
        AUTHORS ChangeLog ChangeLog.46 NEWS README TODO

%find_lang %{name}
%find_lang %{name}_document

%post doc
if [ -f %{_infodir}/texinfo ]; then # --excludedocs?
    /sbin/install-info %{_infodir}/texinfo %{_infodir}/dir || :
fi

%preun doc
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/texinfo ]; then # --excludedocs?
        /sbin/install-info --delete %{_infodir}/texinfo %{_infodir}/dir || :
    fi
fi

%post -n info-doc
if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
    /sbin/install-info %{_infodir}/info-stnd.info %{_infodir}/dir
fi
if [ -x /bin/sed ]; then
    /bin/sed -i '/^This is.*produced by makeinfo.*from/d' %{_infodir}/dir || :
fi

%preun -n info-doc
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/info-stnd.info ]; then # --excludedocs?
        /sbin/install-info --delete %{_infodir}/info-stnd.info %{_infodir}/dir \
        || :
    fi
fi


%files -f %{name}.lang -f %{name}_document.lang
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/makeinfo
%{_bindir}/texi2any
%{_bindir}/pod2texi
%{_datadir}/texinfo
%{_infodir}/texinfo*

%files doc
%defattr(-,root,root,-)
%{_infodir}/%{name}*.*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man5/%{name}.5*
%{_mandir}/man1/texi2any.1*
%{_mandir}/man1/pod2texi.1*

%{_docdir}/%{name}-%{version}

%files -n info
%defattr(-,root,root,-)
%config(noreplace) %verify(not md5 size mtime) %{_infodir}/dir
%license COPYING
%{_bindir}/info
/sbin/install-info

%files -n info-doc
%defattr(-,root,root,-)
%{_infodir}/info-stnd.info*
%{_mandir}/man1/info.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*

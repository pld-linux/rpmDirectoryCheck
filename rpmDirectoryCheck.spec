Summary:	A QA tool to check a large set of RPM-packages for packaging errors
Summary(pl.UTF-8):	Narzędzie QA do sprawdzania dużego zbioru pakietów RPM pod kątem błędów pakietowania
Name:		rpmDirectoryCheck
Version:	0.8.3
Release:	0.1
License:	GPL
Group:		Development/Tools
Source0:	http://enrico-scholz.de/rpmDirectoryCheck/files/%{name}-%{version}.tar.bz2
# Source0-md5:	71028282c5cfd6c8b7a9104c3cc001fb
URL:		http://enrico-scholz.de/rpmDirectoryCheck/
BuildRequires:	graphviz
BuildRequires:	libxslt
BuildRequires:	python
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo-texi2dvi
#Suggests:	graphviz
Requires:	libxslt
Requires:	python-rpm
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This program was designed to find RPM-packages which are putting files
into directories without owning this directories. This practice
creates warnings while upgrading packages in the best case. In the
worst case you will have a lot of orphaned directories and wasted
inodes after deleting a package.

As a side-effect the directory-checker can create a graphical
representation of a package and its requirements.

%description -l pl.UTF-8
Ten program został zaprojektowany do znajdowania pakietów RPM
umieszczających pliki w katalogach bez zawierania tych katalogów. Ta
praktyka powoduje w najlepszym wypadku ostrzeżenia podczas
uaktualniania pakietów. W najgorszym wypadku zostajemy z wieloma
osieroconymi katalogami i zmarnowanymi i-węzłami po usunięciu pakietu.

Jako efekt uboczny program może tworzyć graficzną reprezentację
pakietu i jego zależności.

%prep
%setup -q
%{__sed} -i -e '1s,#!.*bin/python2,#!%{_bindir}/python,'#! src/*.py

%build
%configure
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for i in $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/*.conf; do
	test -e "$i" || continue
	touch $i{o,c}
done

%py_postclean %{_datadir}/rpmDirectoryCheck

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%preun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%doc sample/generate.sh
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%ghost %{_sysconfdir}/%{name}/*.confc
%ghost %{_sysconfdir}/%{name}/*.confo
%attr(755,root,root) %{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/%{name}

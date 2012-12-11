%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Simple database library
Name:		sdb
Version:	0.10.1
Release:	1
License:	GPL
Group:		System/Libraries
URL:		http://siag.nu/libsdb/
Source0:	http://siag.nu/pub/libsdb/%{name}-%{version}.tar.gz
Patch0:		sdb-0.6.0-no_ms.diff
Patch1:		sdb-0.6.0-postgres.diff
BuildRequires:	mysql-devel
BuildRequires:	gdbm-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	postgresql-devel
BuildRequires:	sqlite-devel
BuildRequires:	unixODBC-devel
BuildRequires:	zlib-devel
BuildRequires:	multiarch-utils >= 1.0.3

%description
This is libsdb, the simple database library, which provides a way 
to support multiple database management systems in an application 
with negligeable overhead, in terms of code as well as system 
resources. It is mainly intended for use on Unix, but the ODBC 
driver works on Windows as well. 

%package -n	%{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries

%description -n	%{libname}
This package contains libraries necessary for %{name}.

%package -n	%{develname}
Summary:	Development header files and libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	mysql-devel
Requires:	gdbm-devel
Requires:	openssl-devel
Requires:	postgresql-devel
Requires:	sqlite-devel
Requires:	unixODBC-devel
Requires:	zlib-devel
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name} 0 -d}

%description -n	%{develname}
This package contains the development header files and libraries
for %{name}.

%prep

%setup -q
%patch0 -p0
%patch1 -p0

perl -pi -e "s|/usr/local/|%{_prefix}/|g" configure
perl -pi -e "s|/lib |%{_lib} |g" configure

%build

# the author dropped automake !!!
# ulric blev lite lack på automake tror jag...

./configure \
    --with-gdbm \
    --with-mysql \
    --with-postgres \
    --with-odbc=odbc \
    --with-sqlite

perl -pi -e "s|/sbin/ldconfig|#/sbin/ldconfig|g" Makefile

make CFLAGS="%{optflags} -fPIC "\
    LDFLAGS="%ldflags" \
    PREFIX=%{_prefix} \
    BINDIR=%{_bindir} \
    LIBDIR=%{_libdir} \
    MANDIR=%{_mandir} \
    INCDIR=%{_includedir}

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_mandir}
install -d %{buildroot}%{_includedir}

make \
    PREFIX=%{buildroot}%{_prefix} \
    BINDIR=%{buildroot}%{_bindir} \
    LIBDIR=%{buildroot}%{_libdir} \
    MANDIR=%{buildroot}%{_mandir} \
    INCDIR=%{buildroot}%{_includedir} \
    install

%multiarch_binaries %{buildroot}%{_bindir}/sdb-config

# remove invalid manpages
rm -f %{buildroot}%{_mandir}/man3/sdb_*

%files -n %{name}
%doc AUTHORS COPYING* ChangeLog INSTALL README*
%{_bindir}/sdb_client
%{_bindir}/sdbd
%{_bindir}/sdbd_client
%{_mandir}/man3/sdb.3*
%{_mandir}/man8/sdbd.8*

%files -n %{libname}
%{_libdir}/*.so.*

%files -n %{develname}
%{multiarch_bindir}/sdb-config
%{_bindir}/sdb-config
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*.h


%changelog
* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10.0-8mdv2011.0
+ Revision: 627287
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.0-7mdv2011.0
+ Revision: 626561
- rebuilt against mysql-5.5.8 libs

* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.0-5mdv2011.0
+ Revision: 614829
- the mass rebuild of 2010.1 packages

* Mon Apr 12 2010 Funda Wang <fwang@mandriva.org> 0.10.0-4mdv2010.1
+ Revision: 533652
- use ldflags

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 0.10.0-3mdv2010.1
+ Revision: 507509
- rebuild

* Tue Sep 08 2009 Thierry Vignaud <tv@mandriva.org> 0.10.0-2mdv2010.0
+ Revision: 433636
- rebuild

* Fri Jul 11 2008 Oden Eriksson <oeriksson@mandriva.com> 0.10.0-1mdv2009.0
+ Revision: 233776
- 0.10.0

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0.6.0-9mdv2008.1
+ Revision: 140782
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 09 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-9mdv2008.0
+ Revision: 83635
- new devel naming


* Fri Jan 19 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-8mdv2007.0
+ Revision: 110671
- Import sdb

* Fri Jan 19 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-8mdv2007.1
- rebuilt against new postgresql libs
- bunzip the patches

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-7mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-6mdk
- rebuilt against openssl-0.9.8a

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-5mdk
- rebuilt against MySQL-5.0.15

* Thu Apr 21 2005 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-4mdk
- rebuilt against new postgresql libs

* Wed Jan 26 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.6.0-3mdk
- really fix conditional %%multiarch :)

* Tue Jan 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.6.0-2mdk
- fix deps and conditional %%multiarch

* Tue Jan 25 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.6.0-1mdk
- 0.6.0
- fix patches, build and spec file
- rebuilt against MySQL-4.1.x system libs

* Fri Dec 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.5-3mdk
- revert latest "lib64 fixes"

* Tue Dec 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.5-2mdk
- lib64 fixes

* Mon Jun 14 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.5-1mdk
- 0.5.5
- rebuilt against new deps and with gcc v3.4.x
- merge the static devel sub package into the devel sub package
- added sqlite support
- make it compile (P1)
- fix deps

* Sat Apr 24 2004 Guillaume Cottenceau <gc@mandrakesoft.com> 0.5.4-1mdk
- new version (0.5.3 is an addition by myself, yo - adds support for
  persistent connections in the postgres driver)


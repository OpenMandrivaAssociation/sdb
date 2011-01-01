%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Simple database library
Name:		sdb
Version:	0.10.0
Release:	%mkrel 8
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot}

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

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{name}
%defattr(-,root,root)
%doc AUTHORS COPYING* ChangeLog INSTALL README*
%{_bindir}/sdb_client
%{_bindir}/sdbd
%{_bindir}/sdbd_client
%{_mandir}/man3/sdb.3*
%{_mandir}/man8/sdbd.8*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/sdb-config
%{_bindir}/sdb-config
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*.h

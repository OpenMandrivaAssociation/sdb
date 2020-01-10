Name:		sdb
Summary:	SDB client
Version:	2.1.23
Release:	4
Group:		Development/Other
License:	Apache-2.0
Source0:	%{name}_%{version}.tar.gz

Requires:	udev
BuildRequires:	ncurses-devel

%description
SDB client which communicate with sdbd daemon on Tizen device

%prep
%setup -q -n %{name}-%{version}
%autopatch -p1

%build
%make CC=%{__cc} TARGET_HOST=true MODULE=sdb

%install
%makeinstall_std TARGET_HOST=true MODULE=sdb

%files
%{_bindir}/%{name}
%{_sysconfdir}/udev/rules.d/99-%{name}.rules

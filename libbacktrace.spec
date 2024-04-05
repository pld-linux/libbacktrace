#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Library to produce symbolic backtraces
Summary(pl.UTF-8):	Biblioteka do tworzenia symbolicznych backtrace'ów
Name:		libbacktrace
# "1.0" according to README
Version:	1.0
%define	gitref	7ead8c1ea2f4aeafe9c5b9ef8a9461a9ba781aa8
%define	snap	20240309
Release:	0.%{snap}.1
License:	BSD
Group:		Libraries
Source0:	https://github.com/ianlancetaylor/libbacktrace/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	8681498a6ba92d12609151e3b5411909
URL:		https://github.com/ianlancetaylor/libbacktrace
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libbacktrace library may be linked into a C/C++ program or library
and used to produce symbolic backtraces.

Sample uses would be to print a detailed backtrace when an error
occurs or to gather detailed profiling information.

%description -l pl.UTF-8
Biblioteka libbacktrace może być dołączona do programu lub biblioteki
C/C++ w celu tworzenia symbolicznych backtrace'ów.

Przykładowe zastosowania to wypisywanie szczegółowych śladów wywołań w
przypadku wystąpienia błędu albo zbierania szczegółowych informacji do
profilowania.

%package devel
Summary:	Header files for libbacktrace library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbacktrace
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libbacktrace library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbacktrace.

%package static
Summary:	Static libbacktrace library
Summary(pl.UTF-8):	Statyczna biblioteka libbacktrace
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbacktrace library.

%description static -l pl.UTF-8
Statyczna biblioteka libbacktrace.

%prep
%setup -q -n %{name}-%{gitref}

%build
%configure \
	--enable-shared \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbacktrace.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libbacktrace.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbacktrace.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbacktrace.so
%{_includedir}/backtrace.h
%{_includedir}/backtrace-supported.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbacktrace.a
%endif

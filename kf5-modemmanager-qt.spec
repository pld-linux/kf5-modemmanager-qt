#
# Conditional build:
%bcond_with	tests		# build without tests
#
%define		kdeframever	5.39
%define		qtver		5.3.2
%define		kfname		modemmanager-qt
Summary:	Qt wrapper for ModemManager DBus API
Name:		kf5-%{kfname}
Version:	5.39.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	aceb0cc12f27caaec633c6a3ef44c316
URL:		http://www.kde.org/
BuildRequires:	ModemManager-devel
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Qt wrapper for ModemManager DBus API.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libKF5ModemManagerQt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5ModemManagerQt.so.6

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5ModemManagerQt.so
%{_includedir}/KF5/ModemManagerQt
%{_includedir}/KF5/modemmanagerqt_version.h
%{_libdir}/cmake/KF5ModemManagerQt
%{_libdir}/qt5/mkspecs/modules/qt_ModemManagerQt.pri

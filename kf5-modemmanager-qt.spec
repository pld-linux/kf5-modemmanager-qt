#
# Conditional build:
%bcond_with	tests		# build without tests
#
%define		kdeframever	5.84
%define		qtver		5.9.0
%define		kfname		modemmanager-qt
Summary:	Qt wrapper for ModemManager DBus API
Name:		kf5-%{kfname}
Version:	5.84.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	0433687883ec28733adf7fab3684e0db
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
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	ninja
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
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%{?with_tests:%ninja_build test}

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libKF5ModemManagerQt.so.*.*.*
%ghost %{_libdir}/libKF5ModemManagerQt.so.6
%{_datadir}/qlogging-categories5/modemmanagerqt.categories
%{_datadir}/qlogging-categories5/modemmanagerqt.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5ModemManagerQt.so
%{_includedir}/KF5/ModemManagerQt
%{_includedir}/KF5/modemmanagerqt_version.h
%{_libdir}/cmake/KF5ModemManagerQt

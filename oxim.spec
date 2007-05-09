%define version      1.1.3
%define release      %mkrel 1

%define libname_orig lib%{name}
%define libname %mklibname %{name} 0

Summary:    Another Input Method for traditional Chinese
Name:       oxim
Version:    %{version}
Release:    %{release}
License:    GPL
Group:      System/Internationalization
URL:        http://opendesktop.org.tw/demopage/oxim/
Source0:    ftp://140.111.128.66/odp/OXIM/Source/%{name}-%{version}.tar.gz
Source1:    oxim_README.en

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes:       xcin >= 3.0.0
Provides:        xcin >= 3.0.0
Requires:        zlib
Requires:		%{libname} = %{version}-%{release}
Requires:        libchewing-data
BuildRequires:   zlib-devel
BuildRequires:   gtk2-devel
#BuildRequires:   libtabe-devel db4.3-devel
#BuildRequires:	tabe-devel >= 0.2.6-7mdv
#BuildRequires:	db-devel
BuildRequires:   libchewing-devel
BuildRequires:   qt3-devel
BuildRequires:   X11-devel

%description
Another Input Method for traditional Chinese.


%package -n %{libname}
Summary:    Oxim library
Group:      System/Internationalization
Provides:   %{libname_orig} = %{version}-%{release}

%description -n %{libname}
Oxim library.

%package    qtimm
Summary:    Oxim plugin for qt-immodule
Group:      System/Internationalization
Requires:   %{name} = %{version}

%description qtimm
Oxim plugin for qt-immodule.

%prep
%setup -q

sed -i 's/${qt_dir}\/plugins\/inputmethods/${qt_dir}\/plugins\/%(echo %_lib)\/inputmethods/' configure configure.ac
sed -i 's/$(QTDIR)\/lib/$(QTDIR)\/%(echo %_lib)/' src/qt-immodule/Makefile.in src/qt-immodule/Makefile.am

cp %SOURCE1 README.en

%build
#%configure2_5x --with-tabe-data=%{_libdir}/tabe --disable-static --with-tabe-lib=%_libdir
%configure2_5x --disable-static
%make

%install
%makeinstall_std

# remove devel files
rm -rf %{buildroot}/%{_libdir}/*.{a,la}
rm -rf %{buildroot}/%{_libdir}/gtk-2.0/immodules/*.{a,la}
rm -rf %{buildroot}/%{_libdir}/oxim/modules/*.{a,la}
rm -rf %{buildroot}/%{_sysconfdir}/X11/xinit/xinput.d/%{name}

%post
/sbin/ldconfig
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%postun
/sbin/ldconfig
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib

%clean 
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc README README.en COPYING AUTHORS
%dir %{_sysconfdir}/oxim
%config(noreplace) %{_sysconfdir}/oxim/*
%{_bindir}/oxim*
%{_libdir}/gtk-2.0/immodules/gtk-im-oxim.so
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.so
%dir %{_libdir}/%{name}/immodules
%{_libdir}/%{name}/immodules/gtk*
%{_libdir}/%{name}/panels/*
%{_libdir}/%{name}/tables/*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/liboxim.so*

%files qtimm
%defattr(-,root,root)
%doc COPYING
%dir %{_libdir}/%{name}/immodules
%{_libdir}/%{name}/immodules/qt*
%{qt3plugins}/inputmethods/*.so

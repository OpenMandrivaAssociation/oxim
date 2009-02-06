%define version      1.2.1
%define release      %mkrel 2

%define libname %mklibname %{name} 0
%define develname %mklibname -d %{name}

Summary:	Another Input Method for traditional Chinese
Name:		oxim
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		System/Internationalization
URL:		http://opendesktop.org.tw/demopage/oxim/
Source0:	ftp://140.111.128.66/odp/OXIM/Source/%{name}-%{version}.tar.gz
Source1:	oxim_README.en
Patch0:		oxim-1.2.1-fix-str-fmt.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	zlib
Requires:	%{libname} = %{version}-%{release}
Requires:	libchewing-data
BuildRequires:	zlib-devel
BuildRequires:	gtk2-devel
BuildRequires:	libchewing-devel
BuildRequires:	qt3-devel
BuildRequires:	X11-devel

%description
Another Input Method for traditional Chinese.

%package -n %{libname}
Summary:    Oxim library
Group:      System/Internationalization

%description -n %{libname}
Oxim library.

%package -n %{develname}
Summary:    Oxim Development files
Group:      System/Internationalization
Requires:   %{libname} = %{version}-%{release}
Provides:   %{name}-devel = %{version}-%{release}

%description -n %{develname}
Oxim Development files.

%package    qtimm
Summary:    Oxim plugin for qt-immodule
Group:      System/Internationalization
Requires:   %{name} = %{version}

%description qtimm
Oxim plugin for qt-immodule.

%prep
%setup -q
%patch0 -p0

cp %SOURCE1 README.en

%build
%configure2_5x --disable-static --with-qt-dir=%{qt3dir} --with-qt-imdir=%{qt3plugins}/inputmethods
%make

%install
rm -fr %buildroot
%makeinstall_std

%find_lang %name

# remove devel files
rm -rf %{buildroot}/%{_libdir}/*.{a,la}
rm -rf %{buildroot}/%{_libdir}/gtk-2.0/immodules/*.{a,la}
rm -rf %{buildroot}/%{_libdir}/oxim/modules/*.{a,la}
rm -rf %{buildroot}/%{_sysconfdir}/X11/xinit/xinput.d/%{name}
rm -rf %{buildroot}/%{_datadir}/gettext

%post
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib
%if %mdkversion < 200900
%update_menus
%endif

%postun
gtk-query-immodules-2.0 > %{_sysconfdir}/gtk-2.0/gtk.immodules.%_lib
%if %mdkversion < 200900
%clean_menus
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
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
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/liboxim.so.*

%files qtimm
%defattr(-,root,root)
%doc COPYING
%dir %{_libdir}/%{name}/immodules
%{_libdir}/%{name}/immodules/qt*
%{qt3plugins}/inputmethods/*.so

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/liboxim.so

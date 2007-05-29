%define major   1
%define libname %mklibname %{name}_ %{major}

Name:           openh323
Version:        1.18.0
Release:        %mkrel 2
Epoch:          1
Summary:        OpenH323 Library
License:        MPL
Group:          System/Libraries
URL:            http://www.openh323.org/
Source0:        %{name}-%{version}.tar.bz2
Patch0:         openh323-1.19.0.1-mak_files.patch
Patch1:         openh323-1.15.0-libname.diff
Patch2:         openh323-1.15.1-pic.diff
Patch3:         openh323-1.15.1-pwlib.diff
BuildRequires:  autoconf2.5
BuildRequires:  gawk
BuildRequires:  openssl-devel
BuildRequires:  openldap-devel
BuildRequires:  pwlib-devel >= 1.8.4
BuildRequires:  libspeex-devel
#BuildRequires: vpb-devel
BuildRequires:  XFree86-devel
# (oe) these conflicts for now. i was planning to build against them,
# but i save it for a rainy day, or someone else could fix it ;)
BuildConflicts: gsm-devel
BuildConflicts: libilbc-devel
BuildConflicts: vpb-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a Open Source class library for the development of
applications that wish to use the H.323 protocol for multi-media
communications over packet based networks.

%package -n %{libname}
Summary:        OpenH323 Library
Group:          System/Libraries
Provides:       %{name}_%{major} = %{version}-%{release}
Obsoletes:      %{name}_%{major}
Requires:       %{libname}-plugins >= %{version}-%{release}

%description -n %{libname}
The OpenH323 project aims to create a full featured, interoperable,
Open Source implementation of the ITU H.323 teleconferencing protocol
that can be used by personal developers and commercial users without
charge.

%package -n %{libname}-devel
Summary:        OpenH323 development files
Group:          Development/C
Requires:       %{libname} = %{epoch}:%{version}-%{release} 
Provides:       %{name}-devel = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}
Provides:       %{_lib}%{name}-devel = %{version}-%{release}
Obsoletes:      %{name}_%{major}-devel
Provides:       %{name}_%{major}-devel = %{version}-%{release}

%description -n %{libname}-devel
Header files and libraries for developing applications that use
OpenH323.

%package -n %{libname}-plugins
Summary:        Plugins for OpenH323
Group:          System/Libraries
Requires:       %{libname} = %{epoch}:%{version}-%{release}
Obsoletes:      %{libname}-plugins-g726
Provides:       %{libname}-plugins-g726 = %{version}-%{release}
Provides:       lib%{name}-plugins-g726 = %{version}-%{release}
Provides:       %{name}-plugins-g726 = %{version}-%{release}
Obsoletes:      %{libname}-plugins-gsm0610
Provides:       %{libname}-plugins-gsm0610 = %{version}-%{release}
Provides:       lib%{name}-plugins-gsm0610 = %{version}-%{release}
Provides:       %{name}-plugins-gsm0610 = %{version}-%{release}
Obsoletes:      %{libname}-plugins-ilbc
Provides:       %{libname}-plugins-ilbc = %{version}-%{release}
Provides:       lib%{name}-plugins-ilbc = %{version}-%{release}
Provides:       %{name}-plugins-ilbc = %{version}-%{release}
Obsoletes:      %{libname}-plugins-ima
Provides:       %{libname}-plugins-ima = %{version}-%{release}
Provides:       lib%{name}-plugins-ima = %{version}-%{release}
Provides:       %{name}-plugins-ima = %{version}-%{release}
Obsoletes:      %{libname}-plugins-lpc10
Provides:       %{libname}-plugins-lpc10 = %{version}-%{release}
Provides:       lib%{name}-plugins-lpc10 = %{version}-%{release}
Provides:       %{name}-plugins-lpc10 = %{version}-%{release}
Obsoletes:      %{libname}-plugins-speex
Provides:       %{libname}-plugins-speex = %{version}-%{release}
Provides:       lib%{name}-plugins-speex = %{version}-%{release}
Provides:       %{name}-plugins-speex = %{version}-%{release}

%description -n %{libname}-plugins
This package contains all codec plugins for OpenH323 

%prep
%setup -q
%patch0 -p1 -b .mak_files
%patch1 -p0 -b .libname
%patch2 -p0 -b .pic
%patch3 -p0 -b .pwlib

%build
#don't set this otherwise it will be automatically used by pwlib/openh323 build
#system
export RPM_OPT_FLAGS="" 
export OPT_FLAGS="%{optflags} -DLDAP_DEPRECATED"
%define optflags ""
%{__autoconf}
export CXXFLAGS="$OPT_FLAGS -I../include"
%{configure2_5x} \
    --enable-localspeex \
    --enable-h263avcodec
%{__perl} -pi -e 's/\@SHAREDLIBEXT\@/.so/g' Makefile

#parallel build is broken
%{__make} OPTCCFLAGS="$OPT_FLAGS" optshared PREFIX=%{_prefix} OH323_INCDIR=$RPM_BUILD_DIR/%{name}-%{version}/include
#%%make optshared 

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

# fix strange perms
%{_bindir}/find %{buildroot} -type d -perm 0700 -exec chmod 755 {} \;
%{_bindir}/find %{buildroot} -type f -perm 0555 -exec chmod 755 {} \;
%{_bindir}/find %{buildroot} -type f -perm 0444 -exec chmod 644 {} \;

%post -p /sbin/ldconfig -n %{libname}

%postun -p /sbin/ldconfig -n %{libname}

%clean
%{__rm} -rf %{buildroot}

%files -n %{libname}
%defattr(0644,root,root,0755)
%doc *.txt mpl-1.0.htm
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/*.so
%{_includedir}/*
%{_datadir}/openh323

%files -n %{libname}-plugins
%defattr(-,root,root)
%dir %{_libdir}/pwlib/codecs
%dir %{_libdir}/pwlib/codecs/audio
%attr(0755,root,root) %{_libdir}/pwlib/codecs/audio/*.so

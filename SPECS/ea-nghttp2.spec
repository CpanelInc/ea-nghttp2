%define prefix_dir /opt/cpanel/nghttp2
%define ea_openssl_ver 1.1.1d-1

Summary: Meta-package that only requires libnghttp2
Name: ea-nghttp2
Version: 1.51.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4544 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: MIT
Group: Applications/Internet
URL: https://nghttp2.org/
Source0: https://github.com/tatsuhiro-t/nghttp2/releases/download/v%{version}/nghttp2-%{version}.tar.xz
Patch1: 0001-Select-Python3-for-CentOS-8.patch

%if 0%{?rhel} > 7
# In C8 we use system openssl. See DESIGN.md in ea-openssl11 git repo for details
BuildRequires: openssl-devel
BuildRequires: zlib-devel

Requires: ea-libnghttp2%{?_isa} = %{version}-%{release}
Requires: openssl

    %if 0%{?rhel} == 8
BuildRequires: python36
Requires: python36
    %endif

    %if 0%{?rhel} == 9
BuildRequires: python3
Requires: python3
    %endif

BuildRequires: libnghttp2
%else
BuildRequires: ea-openssl11-devel >= %{ea_openssl_ver}
Requires: ea-openssl11
%endif

%description
This package installs no files.  It only requires the libnghttp2 package.


%package -n ea-libnghttp2
Summary: A library implementing the HTTP/2 protocol
Group: Development/Libraries

%description -n ea-libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.


%package -n ea-libnghttp2-devel
Summary: Files needed for building applications with libnghttp2
Group: Development/Libraries
Requires: ea-libnghttp2%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n ea-libnghttp2-devel
The libnghttp2-devel package includes libraries and header files needed
for building applications with libnghttp2.


%prep
%setup -q -n nghttp2-%{version}

%if 0%{?rhel} > 7
%patch1 -p1 -b .python3
%endif

%build
%if 0%{?rhel} < 8
# Build this against our custom ea-openssl11
export OPENSSL_CFLAGS="-I/opt/cpanel/ea-openssl11/include" OPENSSL_LIBS="-L/opt/cpanel/ea-openssl11/lib -lssl -lcrypto"
%endif

mkdir -p $RPM_BUILD_ROOT%{prefix_dir}
./configure --prefix=%{prefix_dir} --disable-python-bindings


# avoid using rpath
sed -i libtool                              \
    -e 's/^runpath_var=.*/runpath_var=/'    \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/'

make %{?_smp_mflags} V=1


%install
%make_install

# not needed on Fedora/RHEL
rm -f "$RPM_BUILD_ROOT%{_libdir}/libnghttp2.la"
rm -f "$RPM_BUILD_ROOT%{_libdir}/libnghttp2.a"

# will be installed via %%doc
rm -f "$RPM_BUILD_ROOT%{_datadir}/doc/nghttp2/README.rst"

# do not install man pages and helper scripts for tools that are not available
rm -fr "$RPM_BUILD_ROOT%{_datadir}/nghttp2"
rm -fr "$RPM_BUILD_ROOT%{_mandir}/man1"

%post -n ea-libnghttp2 -p /sbin/ldconfig

%postun -n ea-libnghttp2 -p /sbin/ldconfig


%check
# test the just built library instead of the system one, without using rpath
export "LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH"
make %{?_smp_mflags} check


%files

%files -n ea-libnghttp2
%{prefix_dir}


%files -n ea-libnghttp2-devel
%{prefix_dir}/include/nghttp2
%{prefix_dir}/lib/pkgconfig
%doc README.rst

%changelog
* Fri Feb 03 2023 Cory McIntire <cory@cpanel.net> - 1.51.0-1
- EA-11210: Update ea-nghttp2 from v1.49.0 to v1.51.0

* Thu Sep 29 2022 Julian Brown <julian.brown@cpanel.net> - 1.49.0-2
- ZC-10009: Add changes so that it builds on AlmaLinux 9

* Mon Aug 22 2022 Cory McIntire <cory@cpanel.net> - 1.49.0-1
- EA-10894: Update ea-nghttp2 from v1.48.0 to v1.49.0

* Mon Jun 27 2022 Cory McIntire <cory@cpanel.net> - 1.48.0-1
- EA-10794: Update ea-nghttp2 from v1.47.0 to v1.48.0

* Mon Feb 28 2022 Cory McIntire <cory@cpanel.net> - 1.47.0-1
- EA-10520: Update ea-nghttp2 from v1.46.0 to v1.47.0

* Thu Oct 21 2021 Cory McIntire <cory@cpanel.net> - 1.46.0-1
- EA-10224: Update ea-nghttp2 from v1.45.1 to v1.46.0

* Mon Oct 04 2021 Cory McIntire <cory@cpanel.net> - 1.45.1-1
- EA-10159: Update ea-nghttp2 from v1.44.0 to v1.45.1

* Mon Jul 19 2021 Cory McIntire <cory@cpanel.net> - 1.44.0-1
- EA-9970: Update ea-nghttp2 from v1.43.0 to v1.44.0

* Thu Feb 04 2021 Tim Mullin <tim@cpanel.net> - 1.43.0-1
- EA-9573: Update ea-nghttp2 from v1.42.0 to v1.43.0

* Tue Dec 01 2020 Julian Brown <julian.brown@cpanel.net> - 1.42.0-2
- ZC-8005: Replace ea-openssl11 with system openssl on C8

* Sun Nov 29 2020 Cory McIntire <cory@cpanel.net> - 1.42.0-1
- EA-9445: Update ea-nghttp2 from v1.41.0 to v1.42.0

* Mon Jun 29 2020 Julian Brown <julian.brown@cpanel.net> - 1.41.0-2
- ZC-6807: Build on CentOS8

* Mon Jun 08 2020 Cory McIntire <cory@cpanel.net> - 1.41.0-1
- EA-9098: Update ea-nghttp2 from v1.40.0 to v1.41.0

* Wed Dec 18 2019 Daniel Muey <dan@cpanel.net> - 1.40.0-2
- ZC-4361: Update ea-openssl requirement to v1.1.1 (ZC-5583)

* Mon Nov 18 2019 Cory McIntire <cory@cpanel.net> - 1.40.0-1
- EA-8749: Update ea-nghttp2 from v1.39.2 to v1.40.0

* Wed Aug 14 2019 Cory McIntire <cory@cpanel.net> - 1.39.2-1
- EA-8611: Update ea-nghttp2 from v1.39.1 to v1.39.2

* Thu Jun 27 2019 Cory McIntire <cory@cpanel.net> - 1.39.1-1
- EA-8548: Update ea-nghttp2 from v1.38.0 to v1.39.1

* Thu May 16 2019 Cory McIntire <cory@cpanel.net> - 1.38.0-1
- EA-8473: Update ea-nghttp2 from v1.32.0 to v1.38.0

* Tue Jul 31 2018 Tim Mullin <tim@cpanel.net> - 1.32.0-1
- EA-7754: Updated from 1.20.0 to 1.32.0

* Mon Mar 20 2018 Cory McIntire <cory@cpanel.net> - 1.20.0-8
- ZC-3552: Added versioning to ea-openssl requirements.

* Tue Jan 30 2018 Dan Muey <dan@cpanel.net> - 1.20.0-7
- ZC-3365: move to /opt

* Tue Jan 30 2018 Dan Muey <dan@cpanel.net> - 1.20.0-6
- EA-7197: remove conflict for libnghttp2 until we can resolve the issus it cause w/ PHP curl

* Thu Sep 28 2017 Dan Muey <dan@cpanel.net> - 1.20.0-5
- EA-6555: add conflict for libnghttp2 since it provides the same stuff

* Thu Sep 07 2017 Dan Muey <dan@cpanel.net> - 1.20.0-4
- EA-6638: bump release prefix to make the EA4 one newer than the typo'd-release-prefix in EA4-experimental

* Thu Jun 08 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 1.20.0-2
- Promotion from EA4 Experimental to Production

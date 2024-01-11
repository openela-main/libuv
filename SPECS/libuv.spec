# Some of the tests do not work with the network-free environment in Koji
# The packager should run `fedpkg local --with tests` on their machine
# before pushing to Koji
%bcond_with tests

Name:           libuv
Epoch:          1
Version:        1.41.1
Release:        1%{?dist}
Summary:        libuv is a multi-platform support library with a focus on asynchronous I/O.

# the licensing breakdown is described in detail in the LICENSE file
License:        MIT and BSD and ISC
URL:            http://libuv.org/
Source0:        http://dist.libuv.org/dist/v%{version}/libuv-v%{version}.tar.gz
Source2:        %{name}.pc.in
Source3:        libuv.abignore

BuildRequires:  autoconf automake libtool
BuildRequires:  gcc

%if %{with tests}
# don't remove network tests
%else
# -- Patches -- #
Patch1:         0001-Disable-failing-network-tests.patch
%endif

%description
libuv is a multi-platform support library with a focus on asynchronous I/O

%package devel
Summary:        Development libraries for libuv
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
Development libraries for libuv

%package static
Summary:        Platform layer for node.js - static library
Requires:       %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}

%description static
Static library (.a) version of libuv.


%prep
%autosetup -n %{name}-v%{version} -p1

%build
./autogen.sh
%configure --disable-silent-rules
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libuv.la

mkdir -p %{buildroot}%{_libdir}/libuv/
install -Dm0644 -t %{buildroot}%{_libdir}/libuv/ %{SOURCE3}

%check
# Tests are currently disabled because some require network access
# Working with upstream to split these out
#./run-tests
#./run-benchmarks

make check

%ldconfig_scriptlets

%files
%doc README.md AUTHORS CONTRIBUTING.md MAINTAINERS.md SUPPORTED_PLATFORMS.md
%doc ChangeLog
%license LICENSE
%{_libdir}/%{name}.so.*
%{_libdir}/libuv/libuv.abignore

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/uv.h
%{_includedir}/uv/

%files static
%{_libdir}/%{name}.a

%changelog
* Mon Jul 12 2021 Zuzana Svetlikova <zsvetlik@redhat.com> - 1:1.41.1-1
- Rebase to 1.41.1
- Change description to reflect upstream
- Resolves: RHBZ1980033

* Mon Jan 25 2021 Zuzana Svetlikova <zsvetlik@redhat.com> - 1:1.40.0-1
- Rebase to 1.40.0
- Resolves: RHBZ#1895872
- Ship libuv-devel

* Wed Sep 23 2020 Honza Horak <hhorak@redhat.com> - 1:1.38.0-2
- Fix max path size by not using _POSIX_PATH_MAX
  Resolves: #1881870
  Fixes: CVE-2020-8252

* Tue Jun 09 2020 Zuzana Svetlikova <zsvetlik@redhat.com> - 1:1.38.0-1
- Update, disable failing tests

* Thu May 28 2020 Zuzana Svetlikova <zsvetlik@redhat.com> - 1:1.37.0-3
- Run tests

* Mon May 11 2020 Zuzana Svetlikova <zsvetlik@redhat.com> - 1:1.37.0-2
- Resolves: RHBZ#1817821
- bump for build

* Mon May 04 2020 Zuzana Svetlikova <zsvetlik@redhat.com> - 1:1.37.0-1
- Resolves: RHBZ#1817821
- Update to 1.37.0
- Add abidiff ignore file

* Mon Oct 08 2018 Jan Staněk <jstanek@redhat.com> - 1:1.23.1-1
- Update to 1.23.1
- Resolves: rhbz#1637000

* Mon Jul 30 2018 Florian Weimer <fweimer@redhat.com> - 1:1.22.0-2
- Rebuild with fixed binutils

* Mon Jul 30 2018 Zuzana Svetlikova ,zsvetlik@redhat.com> - 1.22.0-1
- Update to 1.22.0

* Mon Feb 26 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.19.2-1
- Update to 1.19.2
- https://github.com/libuv/libuv/blob/v1.19.2/ChangeLog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.19.1-2
- Switch to %%ldconfig_scriptlets

* Sat Jan 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.19.1-1
- Update to 1.19.1

* Fri Jan 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.19.0-2
- Revert few commits which cause regression for nodejs

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.19.0-1
- Update to 1.19.0

* Sat Nov 11 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 1:1.16.1-1
- Update to 1.16.1 (rhbz #1512184)

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.16.0-1
- Update to 1.16.0

* Tue Oct 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.15.0-1
- Update to 1.15.0

* Fri Sep 08 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.14.1-1
- Update to 1.14.1
- https://github.com/libuv/libuv/blob/v1.14.1/ChangeLog

* Thu Aug 17 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.14.0-1
- Update to 1.14.0
- https://github.com/libuv/libuv/blob/v1.14.0/ChangeLog

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.12.0-1
- Update to 1.13.1
- https://github.com/libuv/libuv/blob/v1.13.1/ChangeLog

* Thu Jun 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.12.0-1
- Update to 1.12.0
- https://github.com/libuv/libuv/blob/v1.12.0/ChangeLog

* Tue Feb 28 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.11.0-1
- Update to 1.11.0
- https://github.com/libuv/libuv/blob/v1.11.0/ChangeLog

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.10.2-1
- Update to 1.10.2
- Resolves: RHBZ#1395927

* Sat Nov 19 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.10.1-1
- Update to 1.10.1 (RHBZ #1395927)

* Mon Oct 24 2016 Stephen Gallagher <sgallagh@redhat.com> - 1.10.0-1
- Update to 1.10.0
- https://github.com/libuv/libuv/blob/v1.10.0/ChangeLog

* Wed May 18 2016 Stephen Gallagher <sgallagh@redhat.com> - 1.9.1-1
- Update to 1.9.1
- https://github.com/libuv/libuv/blob/v1.9.1/ChangeLog

* Mon May 09 2016 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-1
- Rebase to 1.9.0 to support Node.js 6.x

* Thu Mar 10 2016 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-1
- Rebase to 1.8.0 to support Node.js 5.8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 01 2015 Stephen Gallagher <sgallagh@redhat.com> 1.7.5-1
- Rebase to 1.7.5 to support Node.js 4.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 19 2015 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:1.4.0-1
- rebase to 1.4.0

* Thu Feb 19 2015 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.33-2
- add missing %%{_?isa} to devel requires of main package
- fix some issues with the pkgconfig file and Group reported by Michael Schwendt

* Thu Feb 19 2015 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.33-1
- new upstream release 0.10.33
  https://github.com/joyent/libuv/blob/v0.10.33/ChangeLog
- update URL to point to the new libuv.org

* Wed Nov 19 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.29-1
- new upstream release 0.10.29
  https://github.com/joyent/libuv/blob/v0.10.29/ChangeLog

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.10.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.28-1
- new upstream release 0.10.28
  https://github.com/joyent/libuv/blob/v0.10.28/ChangeLog

* Thu Jul 03 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.27-3
- build static library for rust (RHBZ#1115975)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.10.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.27-1
- new upstream release 0.10.27
  https://github.com/joyent/libuv/blob/v0.10.27/ChangeLog

* Thu Feb 20 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.25-1
- new upstream release 0.10.25
  https://github.com/joyent/libuv/blob/v0.10.25/ChangeLog

* Mon Jan 27 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.23-1
- new upstream release 0.10.23
  https://github.com/joyent/libuv/blob/v0.10.23/ChangeLog

* Thu Dec 19 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.21-1
- new upstream release 0.10.21
  https://github.com/joyent/libuv/blob/v0.10.21/ChangeLog

* Thu Dec 12 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.20-1
- new upstream release 0.10.20
  https://github.com/joyent/libuv/blob/v0.10.20/ChangeLog

* Tue Nov 12 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.19-1
- new upstream release 0.10.19
  https://github.com/joyent/libuv/blob/v0.10.19/ChangeLog

* Fri Oct 18 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.18-1
- new upstream release 0.10.18
  https://github.com/joyent/libuv/blob/v0.10.18/ChangeLog

* Wed Sep 25 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.17-1
- new upstream release 0.10.17
  https://github.com/joyent/libuv/blob/v0.10.17/ChangeLog

* Fri Sep 06 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.15-1
- new upstream release 0.10.15
  https://github.com/joyent/libuv/blob/v0.10.15/ChangeLog

* Tue Aug 27 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.14-1
- new upstream release 0.10.14
  https://github.com/joyent/libuv/blob/v0.10.14/ChangeLog

* Thu Jul 25 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.13-1
- new upstream release 0.10.13
  https://github.com/joyent/libuv/blob/v0.10.13/ChangeLog

* Wed Jul 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.12-1
- new upstream release 0.10.12

* Wed Jun 19 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.11-1
- new upstream release 0.10.11

* Fri May 31 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.9-1
- new upstream release 0.10.9

* Wed May 29 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.8-2
- fix License tag (RHBZ#968226)

* Wed May 29 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.8-1
- new upstream release 0.10.8

* Wed May 29 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.7-1
- new upstream release 0.10.7
- drop upstreamed patch from 0.10.5-2

* Mon May 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.5-3
- don't sed the soname in the spec anymore; the patch takes care of it now
- drop leftover global define for git revision

* Mon May 13 2013 Stephen Gallagher <sgallagh@redhat.com> - 1:0.10.5-2
- Add patch to properly report soname version information
  This patch will be included upstream in 0.10.6 and can be dropped then.
- Remove Bundles(ev) as this has not been true since 0.9.5

* Wed Apr 24 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.5-1
- new upstream release 0.10.5

* Mon Apr 15 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.4-1
- new upstream release 0.10.4
- drop upstreamed patch

* Thu Apr 04 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.3-2
- backport patch that fixes FTBFS in nodejs-0.10.3

* Sun Mar 31 2013 tchollingsworth@gmail.com - 1:0.10.3-1
- rebase to 0.10.3
- upstream now does proper releases

* Tue Mar 12 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1:0.10.0-2.git5462dab
- drop the patchlevel from the SONAME since libuv will retain binary
  compatibility for the life of the 0.10.x series

* Mon Mar 11 2013 Stephen Gallagher <sgallagh@redhat.com> - 1:0.10.0-1.git5462dab
- Upgrade to 0.10.0 release to match stable Node.js release

* Thu Feb 28 2013 Stephen Gallagher <sgallagh@redhat.com> - 1:0.9.4-4.gitdc559a5
- Bump epoch for the version downgrade
- The 0.9.7 version hit the Rawhide repo due to the mass rebuild, we need a
  clean upgrade path.

* Thu Feb 21 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.9.4-3.gitdc559a5
- Revert to version 0.9.4 (since 0.9.7 is breaking builds)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-2.git4ba03dd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.9.7-1.git4ba03dd
- Bump to version included with Node.js 0.9.7

* Wed Dec 26 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.4-0.1.gitdc559a5
- bump to version included with node 0.9.4
- drop upstreamed patch
- respect optflags

* Thu Nov 15 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-0.3.git09b0222
- Add patch to export uv_inet_*

* Wed Nov 14 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-0.2.git09b0222
- Fixes from package review
- Removed doubly-listed include directory
- Update git tarball to the latest upstream code

* Thu Nov 08 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-0.1.gitd56434a
- Initial package

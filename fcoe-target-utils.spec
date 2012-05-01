%define oname rtsadmin

Name:           fcoe-target-utils
License:        AGPLv3
Group:          System Environment/Libraries
Summary:        An administration shell for FCoE storage targets
Version:        1.99.1.git37f175c
Release:        6%{?dist}
# placeholder URL and source entries
# archive created using:
# git clone git://risingtidesystems.com/rtsadmin.git
# cd rtsadmin
# git archive 37f175c --prefix rtsadmin-%{version}/ | gzip > rtsadmin-%{version}.tar.gz
URL:            http://www.risingtidesystems.com/git/
Source:         %{oname}-%{version}.tar.gz
Source1:        fcoe-target.init
Patch1:         rtsadmin-git-version.patch
Patch2:         0001-rename-rtsadmin-to-targetadmin.patch
Patch3:         0002-Remove-ads-from-cli-welcome-msg.-Mention-help-is-ava.patch
Patch4:         0003-change-config-dir-from-.rtsadmin-to-.targetadmin.patch
Patch5:         0004-bundle-lio-utils.patch
Patch6:         0005-fixup-setup.py.patch
Patch7:         0006-Hack.-dump-scripts-aren-t-in-PATH-anymore-so-call-th.patch
Patch8:         0007-ignore-errors-from-failure-to-set-device-attributes.patch
Patch9:         0008-fix-spec_root-path.patch
Patch10:        0009-add-docs.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python-devel python-rtslib python-configshell epydoc
Requires:       python-rtslib python-configshell fcoe-utils
Requires(post): chkconfig
Requires(preun): chkconfig


%description
An administration shell (targetadmin) for RTS TCM/LIO
storage targets, most notably Fiber Channel over Ethernet
(FCoE) targets.

Based on rtsadmin.

%prep
%setup -q -n %{oname}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
%{__python} setup.py build
gzip --stdout targetadmin.8 > targetadmin.8.gz

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
mkdir -p %{buildroot}%{_sysconfdir}/target/backup
mkdir -p %{buildroot}%{_mandir}/man8/
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/fcoe-target
install -m 755 targetadmin.8.gz %{buildroot}%{_mandir}/man8/

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add fcoe-target

%preun
if [ "$1" = 0 ]; then
        /sbin/chkconfig --del fcoe-target
fi


%files
%defattr(-,root,root,-)
%{python_sitelib}
%{_bindir}/targetadmin
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/fcoe-target
%dir %{_sysconfdir}/target/backup
%doc COPYING README
%{_mandir}/man8/targetadmin.8.gz

%changelog
* Thu Aug 25 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-6
* Modify 0009-add-docs.patch to improve targetadmin man page readability

* Thu Aug 25 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-5
- Fix saveconfig by creating /etc/target/backup
- Add targetadmin manpage
- Add patches
 * 0008-fix-spec_root-path.patch
 * 0009-add-docs.patch

* Thu Aug 18 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-4
- Update based on reviewer comments
  - Remove commented-out todo
  - Document full archive-building process
  - Remove license txt from spec file
  - Add chkconfig line to init file
  - Fix changelog versions (1.9.9.1 -> 1.99.1)
  - Remove epydoc runtime dependency
  - Remove "." from summary
  - Remove shebang from imported *.py files

* Tue Aug 2 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-3
- Rename rtsadmin.spec to fcoe-target-utils.spec

* Mon Aug 1 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-2
- Add init script
- Add copyright to .spec
- Add Requires: fcoe-utils
- Add patches
 * 0006-Hack.-dump-scripts-aren-t-in-PATH-anymore-so-call-th.patch
 * 0007-ignore-errors-from-failure-to-set-device-attributes.patch

* Thu Jul 28 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-1
- Rebase to latest git
- Rename package to fcoe-target-utils
- Rename executable to targetadmin
- Add patches
 * 0001-rename-rtsadmin-to-targetadmin.patch
 * 0002-Remove-ads-from-cli-welcome-msg.-Add-mention-of-man-.patch
 * 0003-change-config-dir-from-.rtsadmin-to-.targetadmin.patch
 * 0004-bundle-lio-utils.patch
 * 0005-fixup-setup.py.patch

* Tue May 10 2011 Andy Grover <agrover@redhat.com> - 1.99-1
- Initial packaging

%global debug_package %{nil}

%global commit 3c1cdd3e634bb4668a900d75efd4d6292b8c7d1d
%global commitdate 20241127
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           ipu6-camera-bins
Summary:        Binary library for Intel IPU6
Version:        0.0
Release:        17.%{commitdate}git%{shortcommit}%{?dist}
License:        Proprietary
URL:            https://github.com/intel/ipu6-camera-bins

Source0: https://github.com/intel/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  chrpath

ExclusiveArch:  x86_64

Requires:       gstreamer1-plugins-icamerasrc
Requires:       v4l2-relayd
Requires:       intel-ipu6-kmod >= 0.0-14

# Require the new Fedora linux-firmware intel-vsc-firmware subpackage and
# obsolete but do not provide the 2 old firmware packages
Requires:       intel-vsc-firmware >= 20240513
Obsoletes:      ipu6-camera-bins-firmware < 0.0-11
Obsoletes:      ivsc-firmware < 0.0-10

# For kmod package
Provides:       intel-ipu6-kmod-common = %{version}

%description
This provides the necessary binaries for Intel IPU6, including library and
firmware. The library includes necessary image processing algorithms and
3A algorithm for the camera.


%package devel
Summary:        IPU6 header files for development
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This provides the necessary header files for IPU6 development.

%prep

%setup -q -n %{name}-%{commit}
chrpath --delete lib/*.so.0
chmod +x lib/*.so.0
# Firmware is part of linux-firmware now
rm -r lib/firmware

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
cp -pr include/* %{buildroot}%{_includedir}
cp -pr lib/* %{buildroot}%{_libdir}

pushd %{buildroot}%{_libdir}
  # The .so.0 files have no soname, manually create symlinks for linking
  for i in *.so.0; do
    ln -s $i `echo $i | sed -e "s|\.so\.0|\.so|"`
  done
  # Fix libdir in .pc files
  for i in pkgconfig/*.pc; do
    sed -i -e "s|libdir=\${prefix}/lib|libdir=%{_libdir}|g" "$i"
  done
popd

%files
%license LICENSE
%{_libdir}/*.so.0

%files devel
%{_includedir}/ipu6
%{_includedir}/ipu6ep
%{_includedir}/ipu6epmtl
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Feb  2 2025 Hans de Goede <hdegoede@redhat.com> - 0.0-17.20241127git3c1cdd3
- Add Requires: gstreamer1-plugins-icamerasrc back

* Fri Jan 31 2025 Hans de Goede <hdegoede@redhat.com> - 0.0-16.20241127git3c1cdd3
- Update to latest upstream commit 3c1cdd3e634bb4668a900d75efd4d6292b8c7d1d
- Temporarily drop Requires: gstreamer1-plugins-icamerasrc to break broken
  depenency loop caused by provided libraries soname changes

* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.0-15.20240507git987b09a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.0-14.20240507git987b09a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul  1 2024 Hans de Goede <hdegoede@redhat.com> - 0.0-13.20240507git987b09a
- Add Requires: gstreamer1-plugins-icamerasrc back

* Mon Jul  1 2024 Hans de Goede <hdegoede@redhat.com> - 0.0-12.20240507git987b09a
- Temporarily drop Requires: gstreamer1-plugins-icamerasrc to break
  broken depenency loop caused by ipu6-camera-hal soname change

* Mon Jun 24 2024 Hans de Goede <hdegoede@redhat.com> - 0.0-11.20240507git987b09a
- Update to commit 987b09ad7e6124ab8623a986f92ecb47061b8fa0
- Drop ipu6-camera-bins-firmware and switch to requiring the new
  Fedora linux-firmware intel-vsc-firmware subpackage

* Fri Mar 08 2024 Kate Hsuan <hpa@redhat.com> - 0.0-10.20231027gitaf5ba0c
- Update to the latest upstream commit

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.0-9.20230208git276859f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug 08 2023 Kate Hsuan <hpa@redhat.com> - 0.0-8.20230208git276859f
- Updated to commit 276859fc6de83918a32727d676985ec40f31af2b

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.0-7.20221112git4694ba7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 09 2023 Kate Hsuan <hpa@redhat.com> - 0.0-6.20221112git4694ba7
- Updated dependency settings

* Tue Dec 13 2022 Kate Hsuan <hpa@redhat.com> - 0.0-5.20221112git4694ba7
- Fix indentation.
- Remove unnecessary dir macro.

* Thu Dec 8 2022 Kate Hsuan <hpa@redhat.com> - 0.0-4.20221112git4694ba7
- Add Requires to make sure version lock between main and -devel package.
  Move .a files to -devel package.
  Fix dir settings.
  Remove unnecessary for loop and duplicated commands.

* Mon Dec 5 2022 Kate Hsuan <hpa@redhat.com> - 0.0-3.20221112git4694ba7
- Set correct rpath for every .so files and put the ExclusiveArch to the
  suitable place.

* Tue Nov 22 2022 Kate Hsuan <hpa@redhat.com> - 0.0-2.20221112git4694ba7
- Small tweaks as a result of pkg-review (rf#6474), including
  setup macro parameters, path settings, and dependency settings.

* Thu Nov 17 2022 Kate Hsuan <hpa@redhat.com> - 0.0-1.20221112git4694ba7
- Revision is based on the pkg-review (rf#6474#c2).

* Tue Oct 25 2022 Kate Hsuan <hpa@redhat.com> - 0.0.1
- First commit

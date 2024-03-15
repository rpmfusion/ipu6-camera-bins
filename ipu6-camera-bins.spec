%global debug_package %{nil}

%global commit af5ba0cb4a763569ac7514635013e9d870040bcf
%global commitdate 20231027
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           ipu6-camera-bins
Summary:        Binary library for Intel IPU6
Version:        0.0
Release:        10.%{commitdate}git%{shortcommit}%{?dist}
License:        Proprietary

Source0: https://github.com/intel/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  chrpath
BuildRequires:  patchelf

ExclusiveArch:  x86_64

Requires:       ipu6-camera-bins-firmware
Requires:       ivsc-firmware
Requires:       gstreamer1-plugins-icamerasrc
Requires:       v4l2-relayd
Requires:       intel-ipu6-kmod

# For kmod package
Provides:       intel-ipu6-kmod-common = %{version}

%description
This provides the necessary binaries for Intel IPU6, including library and
firmware. The library includes necessary image processing algorithms and
3A algorithm for the camera.

%package firmware
Summary:        IPU6 firmware

%description firmware
This provides the necessary firmware for Intel IPU6.

%package devel
Summary:        IPU6 header files for development.
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This provides the necessary header files for IPU6 development.

%prep

%setup -q -n %{name}-%{commit}
for i in ipu_tgl ipu_adl ipu_mtl; do
  chrpath --delete lib/$i/*.so
done

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_includedir}
for i in ipu_tgl ipu_adl ipu_mtl; do
  mkdir -p %{buildroot}%{_libdir}/$i
  cp -pr include/$i %{buildroot}%{_includedir}
  cp -pr lib/$i/lib* lib/$i/pkgconfig %{buildroot}%{_libdir}/$i
  patchelf --set-rpath %{_libdir}/$i %{buildroot}%{_libdir}/$i/*.so
  sed -i \
    -e "s|libdir=\${prefix}/lib/$i|libdir=%{_libdir}/$i|g" \
    %{buildroot}%{_libdir}/$i/pkgconfig/*.pc
done

# IPU6 firmwares
install -p -D -m 0644 lib/firmware/intel/ipu6_fw.bin %{buildroot}/usr/lib/firmware/intel/ipu6_fw.bin
install -p -D -m 0644 lib/firmware/intel/ipu6ep_fw.bin %{buildroot}/usr/lib/firmware/intel/ipu6ep_fw.bin
install -p -D -m 0644 lib/firmware/intel/ipu6epadln_fw.bin %{buildroot}/usr/lib/firmware/intel/ipu6epadln_fw.bin
install -p -D -m 0644 lib/firmware/intel/ipu6epmtl_fw.bin %{buildroot}/usr/lib/firmware/intel/ipu6epmtl_fw.bin

%files
%license LICENSE
%dir %{_libdir}/ipu_tgl
%dir %{_libdir}/ipu_adl
%dir %{_libdir}/ipu_mtl
%{_libdir}/ipu_tgl/*.so*
%{_libdir}/ipu_adl/*.so*
%{_libdir}/ipu_mtl/*.so*

%files firmware
%license LICENSE
%dir /usr/lib/firmware
%dir /usr/lib/firmware/intel
/usr/lib/firmware/intel/ipu6_fw.bin
/usr/lib/firmware/intel/ipu6ep_fw.bin
/usr/lib/firmware/intel/ipu6epadln_fw.bin
/usr/lib/firmware/intel/ipu6epmtl_fw.bin

%files devel
%dir %{_includedir}/ipu_tgl
%dir %{_includedir}/ipu_adl
%dir %{_includedir}/ipu_mtl
%dir %{_libdir}/ipu_tgl/pkgconfig
%dir %{_libdir}/ipu_adl/pkgconfig
%dir %{_libdir}/ipu_mtl/pkgconfig
%{_includedir}/ipu_tgl/*
%{_includedir}/ipu_adl/*
%{_includedir}/ipu_mtl/*
%{_libdir}/ipu_tgl/pkgconfig/*
%{_libdir}/ipu_adl/pkgconfig/*
%{_libdir}/ipu_mtl/pkgconfig/*
%{_libdir}/ipu_tgl/*.a
%{_libdir}/ipu_adl/*.a
%{_libdir}/ipu_mtl/*.a


%changelog
* Fri Mar 08 2024 Kate Hsuan <hpa@redhat.com> - 0.0-10.220231027gitaf5ba0c
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

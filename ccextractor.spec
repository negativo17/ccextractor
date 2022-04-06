%define _legacy_common_support 1

%global commit0 67e15aaf80a576f6f9b79442eaa355d544f0d5c2
%global date 20210527
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

Name:       ccextractor
Version:    0.94
Release:    2%{?dist}
Summary:    A closed captions and teletext subtitles extractor for video streams.
License:    GPL
URL:        http://ccextractor.org/

%if 0%{?tag:1}
Source0:    https://github.com/CCExtractor/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
#Source0:    https://github.com/CCExtractor/%{name}/releases/download/v%{version}/%{name}_minimal.tar.gz
%else
Source0:    https://github.com/CCExtractor/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

Patch0:     %{name}-system-libraries-and-cflags.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  freetype-devel
BuildRequires:  libpng-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glfw3)
BuildRequires:  pkgconfig(lept)
BuildRequires:  pkgconfig(tesseract)
BuildRequires:  protobuf-c-devel
BuildRequires:  utf8proc-devel
BuildRequires:  zlib-devel

# FFMpeg 5 is not supported:
BuildRequires:  pkgconfig(libavcodec) >= 58
BuildRequires:  pkgconfig(libavcodec) < 59
BuildRequires:  pkgconfig(libavformat) >= 58
BuildRequires:  pkgconfig(libavformat) < 59
BuildRequires:  pkgconfig(libavutil) >= 56
BuildRequires:  pkgconfig(libavutil) < 57
BuildRequires:  pkgconfig(libswscale) >= 5
BuildRequires:  pkgconfig(libswscale) < 6

# Unbundle!
Provides:       bundled(gpac)
Provides:       bundled(zvbi)

%description
CCExtractor is a tool used to produce subtitles for TV recordings from almost
anywhere in the world. We intend to keep up with all sources and formats.

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

rm -fr src/thirdparty/{freetype,libpng,utf8proc,zlib}
rm -fr OpenBSD mac windows

%build
cd linux
./pre-build.sh

autoreconf -vif

export CFLAGS="%{optflags} -Wno-maybe-uninitialized"
%configure \
  --enable-ffmpeg \
  --enable-hardsubx \
  --enable-ocr \
  --without-rust

%make_build

%install
cd linux
%make_install

%files
%{_bindir}/%{name}

%changelog
* Wed Apr 06 2022 Simone Caronni <negativo17@gmail.com> - 0.94-2
- Rebuild for updated dependencies.

* Sun Mar 13 2022 Simone Caronni <negativo17@gmail.com> - 0.94-1
- Update to 0.94.

* Fri Sep 24 2021 Simone Caronni <negativo17@gmail.com> - 0.93-1
- Update to 0.93.

* Wed Jul 21 2021 Simone Caronni <negativo17@gmail.com> - 0.90-1
- Update to 0.90.

* Sun Jun 20 2021 Simone Caronni <negativo17@gmail.com> - 0.89-4
- Update to final 0.89.

* Thu May 27 2021 Simone Caronni <negativo17@gmail.com> - 0.89-3.20210527git67e15aa
- Update to latest snapshot.

* Fri Mar 26 2021 Simone Caronni <negativo17@gmail.com> - 0.89-2.20210325git19da837
- Update to latest snapshot.

* Thu Jul 16 2020 Simone Caronni <negativo17@gmail.com> - 0.89-1.20200508git33eccce
- Update to latest snapshot.

* Sun Jun 16 2019 Simone Caronni <negativo17@gmail.com> - 0.88-1
- Update to 0.88.

* Wed Apr 03 2019 Simone Caronni <negativo17@gmail.com> - 0.87-2
- Use system libraries.

* Tue Jan 15 2019 Simone Caronni <negativo17@gmail.com> - 0.87-1
- First build.

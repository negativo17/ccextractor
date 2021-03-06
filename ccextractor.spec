%define _legacy_common_support 1

%global commit0 33ecccedce122d7c2a773f354ac8266ff2cefba5
%global date 20200508
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

Name:       ccextractor
Version:    0.89
Release:    1%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:    A closed captions and teletext subtitles extractor for video streams.
License:    GPL
URL:        http://ccextractor.org/

%if 0%{?tag:1}
Source0:    https://github.com/CCExtractor/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%else
Source0:    https://github.com/CCExtractor/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

Patch0:     %{name}-system-libraries-and-cflags.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  freetype-devel
BuildRequires:  libpng-devel
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glfw3)
BuildRequires:  pkgconfig(lept)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(tesseract)
BuildRequires:  protobuf-c-devel
BuildRequires:  utf8proc-devel
BuildRequires:  zlib-devel

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

rm -fr src/{freetype,libpng,utf8proc,zlib}

%build
cd linux
./pre-build.sh

autoreconf -vif

export CFLAGS="%{optflags} -Wno-maybe-uninitialized"
%configure \
  --enable-ffmpeg \
  --enable-hardsubx \
  --enable-ocr

%make_build

%install
cd linux
%make_install

%files
%{_bindir}/%{name}

%changelog
* Thu Jul 16 2020 Simone Caronni <negativo17@gmail.com> - 0.89-1.20200508git33eccce
- Update to latest snapshot.

* Sun Jun 16 2019 Simone Caronni <negativo17@gmail.com> - 0.88-1
- Update to 0.88.

* Wed Apr 03 2019 Simone Caronni <negativo17@gmail.com> - 0.87-2
- Use system libraries.

* Tue Jan 15 2019 Simone Caronni <negativo17@gmail.com> - 0.87-1
- First build.

Name:       ccextractor
Version:    0.88
Release:    1%{?dist}
Summary:    A closed captions and teletext subtitles extractor for video streams.
License:    GPL
URL:        http://ccextractor.org/

Source0:    https://github.com/CCExtractor/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz 

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
BuildRequires:  utf8proc-devel
BuildRequires:  zlib-devel

# Unbundle!
Provides:       bundled(gpac)
Provides:       bundled(protobuf-c)
Provides:       bundled(zvbi)

%description
CCExtractor is a tool used to produce subtitles for TV recordings from almost
anywhere in the world. We intend to keep up with all sources and formats.

%prep
%autosetup -p1
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
* Sun Jun 16 2019 Simone Caronni <negativo17@gmail.com> - 0.88-1
- Update to 0.88.

* Wed Apr 03 2019 Simone Caronni <negativo17@gmail.com> - 0.87-2
- Use system libraries.

* Tue Jan 15 2019 Simone Caronni <negativo17@gmail.com> - 0.87-1
- First build.

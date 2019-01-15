Name:       ccextractor
Version:    0.87
Release:    1
Summary:    A closed captions and teletext subtitles extractor for video streams.
License:    GPL
URL:        http://ccextractor.org/

Source0:    https://github.com/CCExtractor/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz 

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glfw3)
BuildRequires:  pkgconfig(lept)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(tesseract)

BuildRequires:  zlib-devel

# Unbundle!
Provides:       bundled(freetype)
Provides:       bundled(gpac) = 0.7.2
Provides:       bundled(libpng)
Provides:       bundled(protobuf-c)
Provides:       bundled(utf8proc)
Provides:       bundled(zlib)
Provides:       bundled(zvbi)

%description
CCExtractor is a tool used to produce subtitles for TV recordings from almost
anywhere in the world. We intend to keep up with all sources and formats.

%prep
%autosetup

sed -i \
    -e 's/CFLAGS += -s -O3 -DUNIX/CFLAGS += -DUNIX/g' \
    -e 's/CFLAGS += -O3 -s -DGPAC_CONFIG_LINUX/CFLAGS += -DGPAC_CONFIG_LINUX/g' \
    linux/Makefile.am

%build
cd linux
./pre-build.sh

autoreconf -vif

%configure \
  --enable-ffmpeg \
  --enable-hardsubx \
  --enable-ocr

%make_build

%install
cd linux
%make_install
#install -D -m755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}

%changelog
* Tue Jan 15 2019 Simone Caronni <negativo17@gmail.com> - 0.87-1
- First build.

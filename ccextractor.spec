# mock configuration:
# - Requires network for fetching the Rust crates

#global tag %{version}

%global commit0 67e15aaf80a576f6f9b79442eaa355d544f0d5c2
%global date 20210527
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

Name:       ccextractor
Version:    0.96.6
Release:    1%{?dist}
Summary:    A closed captions and teletext subtitles extractor for video streams
License:    GPL-2.0-only
URL:        http://ccextractor.org/

%if 0%{?tag:1}
Source0:    https://github.com/CCExtractor/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%else
Source0:    https://github.com/CCExtractor/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

# Unbundle freetype, libpng, utf8proc and zlib; drop "-O3 -s", it overrides the
# distribution flags and strips the binary at link time.
Patch0:     %{name}-system-libraries.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cargo
# The leptonica-sys crate generates its bindings with bindgen:
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  freetype-devel
BuildRequires:  libpng-devel
BuildRequires:  openssl-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  utf8proc-devel
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glfw3)
BuildRequires:  pkgconfig(gpac)
BuildRequires:  pkgconfig(lept)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavdevice)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(tesseract)

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

# Some are executable and start with "#![...]", which is taken for a shebang:
find src/rust -name '*.rs' -exec chmod -x {} +

# The version is hardcoded in several places and not bumped with the release tag:
sed -i -E 's/^(AC_INIT\(\[CCExtractor\], \[)[0-9.]+/\1%{version}/' linux/configure.ac
sed -i -E 's/^(#define VERSION ")[0-9.]+/\1%{version}/' src/lib_ccx/lib_ccx.h
sed -i -E 's/(command\(version = ")[0-9.]+/\1%{version}/' src/rust/src/args.rs


%build
cd linux
./pre-build.sh
autoreconf -vif

export CFLAGS="%{optflags} -Wno-maybe-uninitialized"
%configure \
    --enable-ffmpeg \
    --enable-hardsubx \
    --enable-ocr \
    --with-rust

%make_build

%install
cd linux
%make_install

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}

%changelog
* Fri Sep 18 2026 Simone Caronni <negativo17@gmail.com> - 0.96.6-1
- Update to 0.96.6.
- Enable the Rust library, gpac is no longer bundled.

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

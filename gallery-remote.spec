#
%define		_base	1.5
%define		_rc		b32
%define		_rel	1
Summary:	Gallery Remote - client-side frontend to Gallery
Summary(pl.UTF-8):	Gallery Remote - frontend do Gallery działający po stronie klienta
Name:		gallery-remote
Version:	1.5.1
Release:	%{_rc}.%{_rel}
License:	GPL v2
Group:		Applications/Publishing
Source0:	http://dl.sourceforge.net/gallery/GalleryRemote.%{_base}.Linux.NoVM.bin
# Source0-md5:	521fb28f0027c4d7c84f7ef26c21b790
Source1:	http://www.gallery2.hu/download/GalleryRemote/gallery_remote_%{version}-%{_rc}.zip
# Source1-md5:	657d766c14a6e7e13b766b92dd67a13f
Source2:	%{name}.png
Source3:	%{name}.desktop
URL:		http://gallery.menalto.com/wiki/Gallery_Remote
BuildRequires:	sed >= 4.0
Requires:	ImageMagick
Requires:	ImageMagick-coder-jpeg
Requires:	ImageMagick-coder-jpeg2
Requires:	ImageMagick-coder-png
Requires:	ImageMagick-coder-tiff
Requires:	jre >= 1.4
Requires:	libjpeg-progs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/%{name}

%description
Gallery Remote is a client-side Java application that provides users
with a rich front-end to Gallery. This application makes it easier to
upload images to your Gallery.

%description -l pl.UTF-8
Gallery Remote to aplikacja w Javie działająca po stronie klienta
udostępniająca użytkownikom bogaty frontend do Gallery. Ta
aplikacja czyni łatwiejszym umieszczanie obrazków w Gallery.

%prep
%setup -qcT

# emulate the self-extractable installer
head -n 256 %{SOURCE0} > header
ARCHREALSIZE=$(awk -F= '/^ARCHREALSIZE=/{print $2}' header)
BLOCKSIZE=$(awk -F= '/^BLOCKSIZE=/{print $2}' header)
RESSIZE=$(awk -F= '/^RESSIZE=/{print $2}' header)
ARCHSTART=$(awk -F= '/^ARCHSTART=/{print $2}' header)
RESOURCE_ZIP=Resource1.zip
INSTALLER_BLOCKS=$(expr $ARCHREALSIZE / $BLOCKSIZE)
INSTALLER_REMAINDER=$(expr $ARCHREALSIZE % $BLOCKSIZE || :)
if [ ${INSTALLER_REMAINDER:-0} -gt 0 ]; then
	INSTALLER_BLOCKS=$(expr $INSTALLER_BLOCKS + 1)
fi
dd if=%{SOURCE0} of="$RESOURCE_ZIP" bs=$BLOCKSIZE skip=`expr $ARCHSTART + $INSTALLER_BLOCKS` count=$RESSIZE

unzip -qq Resource1.zip
mv '$IA_PROJECT_DIR$'/* .

# should overwrite files from 1.5 according to http://gallery.menalto.com/wiki/Gallery_Remote
unzip -qq -o %{SOURCE1}

mv gallery_docs/dist/grpackage html
rm -f LICENSE # GPL v2
rm -rf */{win32,macos} # wrong os

# make it configured
mv imagemagick/im.properties{.preinstalled,}
mv imagemagick/HOWTO HOWTO.imagemagick

# and jpegtran too
mv jpegtran/{linux/,}jpegtran.properties
rm jpegtran/linux/jpegtran # binary
rm jpegtran/jpegtran.preinstalled
rm -rf jpegtran/linux
sed -i -e '/^jp\.path/s/=.*/=jpegtran/' jpegtran/jpegtran.properties
# undos
sed -i -e 's,\r$,,' jpegtran/jpegtran.properties

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -a imagemagick img jpegtran lib $RPM_BUILD_ROOT%{_appdir}
cp -a GalleryRemote.jar $RPM_BUILD_ROOT%{_appdir}
cat <<EOF > $RPM_BUILD_ROOT%{_bindir}/%{name}
#!/bin/sh
cd %{_appdir}
exec java -Xmx1024m -cp GalleryRemote.jar com.gallery.GalleryRemote.GalleryRemote
EOF
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog html
%attr(755,root,root) %{_bindir}/*
%{_appdir}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

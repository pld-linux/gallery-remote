Summary:	Gallery Remote - client-side frontend to Gallery
Summary(pl.UTF-8):   Gallery Remote - frontend do Gallery działający po stronie klienta
Name:		gallery-remote
Version:	1.5
Release:	1
License:	GPL v2
Group:		Applications/Publishing
Source0:	http://dl.sourceforge.net/gallery/GalleryRemote.%{version}.jar
# Source0-md5:	6043106f54f85380b1bbc06d8dd19d4f
Source1:	%{name}.png
Source2:	%{name}.desktop
URL:		http://gallery.menalto.com/modules.php?op=modload&name=phpWiki&file=index&pagename=Gallery%20Remote
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
udostępniająca użytkownikom bogaty frontend do Gallery. Ta aplikacja
czyni łatwiejszym umieszczanie obrazków w Gallery.

%prep
%setup -q -c
install -d gallery_docs
unzip -qq -o Disk1/InstData/Resource1.zip

# use better names
mv '$IA_PROJECT_DIR$' %{name}

cd %{name}

mv gallery_docs/dist/grpackage html
rm -f LICENSE # GPL v2
rm -rf */{win32,macos} # wrong os

# make it configured
mv imagemagick/im.properties{.preinstalled,}
mv imagemagick/HOWTO HOWTO.imagemagick
rm imagemagick/LICENSE # imagemagick license

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
cd %{name}

install -d $RPM_BUILD_ROOT{%{_appdir},%{_bindir},%{_pixmapsdir},%{_desktopdir}}
cp -a imagemagick img jpegtran lib $RPM_BUILD_ROOT%{_appdir}
cp -a *.jar $RPM_BUILD_ROOT%{_appdir}
cat <<EOF > $RPM_BUILD_ROOT%{_bindir}/%{name}
#!/bin/sh
cd %{_appdir}
exec java -cp GalleryRemote.jar com.gallery.GalleryRemote.GalleryRemote
EOF
install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{name}/{ChangeLog,README,HOWTO.imagemagick,html}
%attr(755,root,root) %{_bindir}/*
%{_appdir}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

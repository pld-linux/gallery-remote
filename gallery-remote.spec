Summary:	Gallery Remote
Name:		gallery-remote
Version:	1.4.1
Release:	0.1
License:	GPL
Group:		Applications/Publishing
Source0:	http://dl.sourceforge.net/gallery/GalleryRemote.%{version}.Linux.NoVM.bin
# Source0-md5:	ad84576e9dedb24fdf3c5b90cd3003ef
URL:		http://gallery.menalto.com/modules.php?op=modload&name=phpWiki&file=index&pagename=Gallery%20Remote
BuildArch:	noarch
Requires:	jre >= 1.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_datadir}/%{name}

%description
Gallery Remote is a client-side Java application that provides users
with a rich front-end to Gallery. This application makes it easier to
upload images to your Gallery.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

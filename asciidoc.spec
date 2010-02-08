Name:       asciidoc
Version:    8.5.3
Release:    %mkrel 1

Summary:    Tool to convert AsciiDoc text files to DocBook, HTML or Unix man pages
License:    GPL
Group:      Publishing
Url:        http://www.methods.co.nz/asciidoc/
Source0:    http://downloads.sourceforge.net/project/asciidoc/asciidoc/%{version}/asciidoc-%{version}.tar.gz
Patch0:     asciidoc-8.5.3-fix_makefile.patch
BuildRequires: python-devel

BuildArch: noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}

Requires: python
# For a2x
Suggests:   dblatex
Suggests:   fop
Suggests:   w3m
Suggests:   xsltproc

%description
AsciiDoc is a text document format for writing short documents, articles,
books and UNIX man pages.

%prep
%setup -q
#sed -i -e "s|CONFDIR=.*|CONFDIR=%{buildroot}%{_sysconfdir}/asciidoc|" \
#-e "s|BINDIR=.*|BINDIR=%{buildroot}%{_bindir}|" \
#-e "s|MANDIR=.*|MANDIR=%{buildroot}%{_mandir}|" \
#-e "s|VIM_CONFDIR=.*|VIM_CONFDIR=%{buildroot}%{_sysconfdir}/vim|" \
#install-sh
%patch0 -p0

%build
%configure
%make

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%makeinstall_std

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc BUGS CHANGELOG COPYRIGHT README
%doc doc/*.txt filters/*/*.txt
%doc %{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/asciidoc/
%{_bindir}/asciidoc.py
%{_bindir}/asciidoc
%{_bindir}/a2x.py
%{_bindir}/a2x

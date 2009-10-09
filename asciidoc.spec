Summary: Tool to convert AsciiDoc text files to DocBook, HTML or Unix man pages
Name: asciidoc
Version: 8.2.7
Release: %mkrel 3
License: GPL
Group: Publishing
URL: http://www.methods.co.nz/asciidoc/

Source: http://www.methods.co.nz/asciidoc/asciidoc-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: python-devel
Requires: python
# For a2x
Suggests: xsltproc dblatex w3m fop

%description
AsciiDoc is a text document format for writing short documents, articles,
books and UNIX man pages.

%prep
%setup -q
sed -i -e "s|CONFDIR=.*|CONFDIR=%{buildroot}%{_sysconfdir}/asciidoc|" \
-e "s|BINDIR=.*|BINDIR=%{buildroot}%{_bindir}|" \
-e "s|MANDIR=.*|MANDIR=%{buildroot}%{_mandir}|" \
-e "s|VIM_CONFDIR=.*|VIM_CONFDIR=%{buildroot}%{_sysconfdir}/vim|" \
install.sh

%build

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
./install.sh

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc BUGS CHANGELOG COPYRIGHT README
%doc doc/*.txt filters/*.txt
%doc %{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/asciidoc/
%{_bindir}/asciidoc
%{_bindir}/a2x

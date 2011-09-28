Name:       asciidoc
Version:    8.6.6
Release:    1

Summary:    Tool to convert AsciiDoc text files to DocBook, HTML or Unix man pages
License:    GPLv2+
Group:      Publishing
Url:        http://www.methods.co.nz/asciidoc/
Source0:    http://downloads.sourceforge.net/project/asciidoc/asciidoc/%{version}/asciidoc-%{version}.tar.gz
Patch0:     asciidoc-8.5.3-fix_makefile.patch
BuildRequires: python-devel dos2unix
BuildRequires: docbook-dtd42-xml
BuildRequires: docbook-dtd43-xml
BuildRequires: docbook-dtd44-xml
BuildRequires: docbook-dtd45-xml
BuildRequires: xsltproc

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
%patch0 -p0

for i in CHANGELOG README; 
do
    iconv -f ISO-8859-1 -t UTF-8 -o $i.UTF-8 $i
    mv  $i.UTF-8 $i
done
for i in  doc/book-multi.txt doc/article.txt COPYRIGHT doc/faq.txt filters/code/code-filter-readme.txt \
doc/asciidoc.1.txt filters/code/code-filter-test.txt doc/book.txt doc/latex-backend.txt;
do  
    dos2unix < $i > $i.fixed ; mv -f $i.fixed $i ;
done

%build
%configure2_5x
sed -ri 's/a2x.py -f/a2x.py -v -f/g' Makefile
%make

%install
%{__rm} -rf %{buildroot}
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

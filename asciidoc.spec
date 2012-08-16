Summary:	Tool to convert AsciiDoc text files to DocBook, HTML or Unix man pages
Name:		asciidoc
Version:	8.6.8
Release:	1
License:	GPLv2+
Group:		Publishing
Url:		http://www.methods.co.nz/asciidoc/
Source0:	http://downloads.sourceforge.net/project/asciidoc/asciidoc/%{version}/asciidoc-%{version}.tar.gz
Patch0:		asciidoc-8.5.3-fix_makefile.patch
#From Fedora
Patch1:		asciidoc-8.6.6-datadir.patch
BuildRequires:	python-devel
BuildRequires:	dos2unix
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-dtd43-xml
BuildRequires:	docbook-dtd44-xml
BuildRequires:	docbook-dtd45-xml
BuildRequires:	xsltproc
BuildArch:	noarch
Requires:	python
# For a2x
Suggests:	dblatex
Suggests:	fop
Suggests:	w3m
Suggests:	xsltproc
Conflicts:	%{name} <= 8.6.5

%description
AsciiDoc is a text document format for writing short documents, articles,
books and UNIX man pages.

%prep
%setup -q
%apply_patches

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
%makeinstall_std

# real conf data goes to sysconfdir, rest to datadir; symlinks so asciidoc works
for d in dblatex docbook-xsl images javascripts stylesheets; do
    mv %{buildroot}%{_sysconfdir}/asciidoc/$d \
        %{buildroot}%{_datadir}/asciidoc
    ln -s %{_datadir}/asciidoc/$d %{buildroot}%{_sysconfdir}/asciidoc/
done

# Python API
install -Dpm 644 asciidocapi.py %{buildroot}%{python_sitelib}/asciidocapi.py

# Make it easier to %exclude these with both rpm < and >= 4.7
for file in %{buildroot}{%{_bindir},%{_datadir}/asciidoc/filters/*}/*.py ; do
    rm -f ${file}{c,o}
done

%files
%doc BUGS CHANGELOG COPYRIGHT README
%doc doc/*.txt filters/*/*.txt
%doc %{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/asciidoc/
%{_bindir}/asciidoc.py
%{_bindir}/asciidoc
%{_bindir}/a2x.py
%{_bindir}/a2x
%{_datadir}/asciidoc/
%{python_sitelib}/asciidocapi.py*

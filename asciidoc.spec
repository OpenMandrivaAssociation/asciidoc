Name:		asciidoc
Version:	8.6.8
Release:	3

Summary:	Tool to convert AsciiDoc text files to DocBook, HTML or Unix man pages
License:	GPLv2+
Group:		Publishing
Url:		http://www.methods.co.nz/asciidoc/
Source0:	http://downloads.sourceforge.net/project/asciidoc/asciidoc/%{version}/asciidoc-%{version}.tar.xz
Patch0:		asciidoc-8.6.8-datadir.patch
BuildRequires:	python-devel
BuildRequires:	dos2unix
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-dtd43-xml
BuildRequires:	docbook-dtd44-xml
BuildRequires:	docbook-dtd45-xml
BuildRequires:	xsltproc

BuildArch:	noarch


%description
AsciiDoc is a text document format for writing short documents, articles,
books and UNIX man pages.

%package -n a2x
Summary:	Converts Asciidoc text files to other formats (PDF, EPUB, DVI, etc.)
Group:		Publishing
Requires:	asciidoc
Suggests:	dblatex
Suggests:	fop
Suggests:	w3m
Suggests:	xsltproc

%description -n a2x
A toolchain manager for AsciiDoc that converts Asciidoc text files to other
file formats.

%prep
%setup -q
%patch0 -p1

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
install -Dpm 644 asciidocapi.py %{buildroot}%{py_puresitedir}/asciidocapi.py

# Make it easier to %exclude these with both rpm < and >= 4.7
for file in %{buildroot}{%{_bindir},%{_datadir}/asciidoc/filters/*}/*.py ; do
    rm -f ${file}{c,o}
done

%files
%doc BUGS CHANGELOG COPYRIGHT README
%doc doc/*.txt filters/*/*.txt
%doc %{_mandir}/man1/ascii*
%config(noreplace) %{_sysconfdir}/asciidoc/
%{_bindir}/asciidoc.py
%{_bindir}/asciidoc
%{_datadir}/asciidoc/
%{py_puresitedir}/asciidocapi.py*

%files -n a2x
%{_bindir}/a2x.py
%{_bindir}/a2x
%doc %{_mandir}/man1/a2x*

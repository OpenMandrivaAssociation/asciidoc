%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global vimdir %{_datadir}/vim/vimfiles

Summary: Text based document generation
Name: asciidoc
Version: 8.6.8
Release: 3%{?dist}
# The python code does not specify a version.
# The javascript example code is GPLv2+.
License: GPL+ and GPLv2+


URL: http://www.methods.co.nz/asciidoc/
Source: http://sourceforge.net/projects/asciidoc/files/%{name}/%{version}/%{name}-%{version}.tar.gz

Patch1: 0001-a2x-Write-manifests-in-UTF-8-by-default.patch

BuildRequires: python-devel
BuildRequires: dblatex
BuildRequires: graphviz
BuildRequires: libxslt
BuildRequires: lilypond
BuildRequires: source-highlight
BuildRequires: texlive-dvipng.bin
BuildRequires: vim-common


Requires: python >= 2.4
Requires: docbook-style-xsl
Requires: graphviz
Requires: libxslt
Requires: libxslt
Requires: source-highlight
Requires: vim-common

BuildArch: noarch

%description
AsciiDoc is a text document format for writing short documents,
articles, books and UNIX man pages. AsciiDoc files can be translated
to HTML and DocBook markups using the asciidoc(1) command.

%package doc
Summary:  Additional documentation and examples for asciidoc
Requires: %{name} = %{version}-%{release}

%description doc
%{summary}.

%package latex
Summary:  Support for asciidoc latex output
Requires: %{name} = %{version}-%{release}
Requires: dblatex
Requires: texlive-dvipng.bin

%description latex
%{summary}.

%package music
Summary:  Support for asciidoc music output
Requires: %{name} = %{version}-%{release}
Requires: lilypond

%description music
%{summary}.


%prep
%setup -q

%patch1 -p1 -b .bz968308

# Fix line endings on COPYRIGHT file
sed -i "s/\r//g" COPYRIGHT

# Convert CHANGELOG and README to utf-8
for file in CHANGELOG README; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

sed -i "s| \(/etc/vim\)|$(DESTDIR)\1|g;" Makefile.in

%build
%configure

%install
make install docs DESTDIR=%{buildroot}

install -dm 755 %{buildroot}%{_datadir}/asciidoc/
# real conf data goes to sysconfdir, rest to datadir; symlinks so asciidoc works
for d in dblatex docbook-xsl images javascripts stylesheets; do
    mv -v %{buildroot}%{_sysconfdir}/asciidoc/$d \
          %{buildroot}%{_datadir}/asciidoc/
    ln -s %{_datadir}/%{name}/$d %{buildroot}%{_sysconfdir}/%{name}/

    # let's symlink stuff for documentation as well so we don't duplicate things
    rm -rf %{buildroot}%{_docdir}/%{name}/$d
    ln -s %{_datadir}/%{name}/$d %{buildroot}%{_docdir}/%{name}/
done

# Python API
install -Dpm 644 asciidocapi.py %{buildroot}%{python_sitelib}/asciidocapi.py

# Make it easier to %exclude these with both rpm < and >= 4.7
for file in %{buildroot}{%{_bindir},%{_sysconfdir}/asciidoc/filters/*}/*.py ; do
    touch ${file}{c,o}
done

mkdir -p %{buildroot}%{vimdir}/{ftdetect,syntax}
for file in $(cd vim; find * -type f); do
    install -m 0644 vim/$file %{buildroot}%{vimdir}/$file
done
install -p -m644 COPYING COPYRIGHT BUGS CHANGELOG README %{buildroot}%{_docdir}/%{name}

%if 0
%check
export PATH="../:$PATH"
cd tests
python testasciidoc.py update
python testasciidoc.py run
%endif

%files
%doc %{_docdir}/%{name}
%exclude %{_docdir}/%{name}/examples
%exclude %{_docdir}/%{name}/doc
%doc %{_mandir}/man1/a2x.1*
%doc %{_mandir}/man1/asciidoc.1*
%{_bindir}/a2x
%{_bindir}/a2x.py
%{_bindir}/asciidoc
%{_bindir}/asciidoc.py
%{_datadir}/asciidoc/
%{python_sitelib}/asciidocapi.py*
%{vimdir}/ftdetect/asciidoc_filetype.vim
%{vimdir}/syntax/asciidoc.vim
%{_bindir}/*.py[co]
%{_sysconfdir}/asciidoc
%exclude %{_sysconfdir}/asciidoc/filters/latex
%exclude %{_sysconfdir}/asciidoc/filters/music

%files doc
%{_docdir}/%{name}/examples
%{_docdir}/%{name}/doc

%files latex
%{_sysconfdir}/asciidoc/filters/latex

%files music
%{_sysconfdir}/asciidoc/filters/music

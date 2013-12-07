Name:		asciidoc
Version:	8.6.8
Release:	4

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

# For a2x
Suggests:	dblatex
Suggests:	fop
Suggests:	w3m
Suggests:	xsltproc

%description
AsciiDoc is a text document format for writing short documents, articles,
books and UNIX man pages.

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




%changelog
* Wed Nov 02 2011 Александр Казанцев <kazancas@mandriva.org> 8.6.6-2
+ Revision: 712312
- move data from /etc to /usr/share
- delete unused python pyc and pyo file

* Wed Sep 28 2011 Andrey Bondrov <abondrov@mandriva.org> 8.6.6-1
+ Revision: 701768
- New version: 8.6.6

* Thu Aug 04 2011 Alexandre Lissy <alissy@mandriva.com> 8.6.5-2
+ Revision: 693243
- Add debug to find where the problem lies with BuildSystem
- Bad guess.
- Release bump
- Disable parallel build

* Thu Aug 04 2011 Alexandre Lissy <alissy@mandriva.com> 8.6.5-1
+ Revision: 693172
- Debug build ...
- Adding BuildRequires for all docbook-dtd4{2,3,4,5}-xml
- Updating to latest release.

* Tue Mar 15 2011 Stéphane Téletchéa <steletch@mandriva.org> 8.6.4-1
+ Revision: 645015
- update to new version 8.6.4

* Tue Dec 07 2010 Funda Wang <fwang@mandriva.org> 8.6.3-1mdv2011.0
+ Revision: 613551
- add BR

  + Sandro Cazzaniga <kharec@mandriva.org>
    - update to 8.6.3

* Wed Aug 25 2010 Lev Givon <lev@mandriva.org> 8.6.1-1mdv2011.0
+ Revision: 573005
- Update to 8.6.1.

* Mon Feb 08 2010 Michael Scherer <misc@mandriva.org> 8.5.3-1mdv2010.1
+ Revision: 501873
- spec file cleaning
- fix License
- update to 8.5.3
- fix Url

  + Jérôme Quelin <jquelin@mandriva.org>
    - reformat spec file

* Fri Oct 09 2009 Pascal Terjan <pterjan@mandriva.org> 8.2.7-3mdv2010.0
+ Revision: 456273
- Install a2x and suggest its dependencies

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 8.2.7-2mdv2010.0
+ Revision: 413038
- rebuild

* Mon Sep 01 2008 Gaëtan Lehmann <glehmann@mandriva.org> 8.2.7-1mdv2009.0
+ Revision: 278295
- update to new version 8.2.7

* Thu Jun 19 2008 Thierry Vignaud <tv@mandriva.org> 8.2.5-2mdv2009.0
+ Revision: 226177
- rebuild

* Fri Dec 28 2007 Gaëtan Lehmann <glehmann@mandriva.org> 8.2.5-1mdv2008.1
+ Revision: 138820
- update to new version 8.2.5

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Jul 24 2007 Gaëtan Lehmann <glehmann@mandriva.org> 8.2.2-1mdv2008.0
+ Revision: 55061
- 8.2.2


* Thu Nov 30 2006 Gaëtan Lehmann (INRA) <glehmann@mandriva.org> 8.1.0-1mdv2007.0
+ Revision: 89051
- 8.1.0

* Thu Aug 10 2006 Gaëtan Lehmann (INRA) <glehmann@mandriva.org> 7.1.2-2mdv2007.0
+ Revision: 55014
- rebuild
- Import asciidoc

* Wed Mar 08 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 7.1.2-1mdk
- New release 7.1.2

* Tue Feb 28 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 7.1.1-1mdk
- New release 7.1.1

* Fri Jan 13 2006 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 7.1.0-1mdk
- New release 7.1.0

* Wed Dec 21 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 7.0.4-2mdk
- rebuild to sync x86_64 package

* Thu Dec 08 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 7.0.4-1mdk
- New release 7.0.4

* Sat Dec 03 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 7.0.3-1mdk
- New release 7.0.3

* Fri Sep 09 2005 Gaetan Lehmann <gaetan.lehmann@jouy.inra.fr> 7.0.2-1mdk
- first mandriva release

* Sat Aug 13 2005 Dag Wieers <dag@wieers.com> - 7.0.1-3 - 3468+/dag
- Add missing deffatr(). (Alain Rykaert)
- Put asciidoc in %%{_bindir}, instead of a symlink.

* Thu Aug 11 2005 Dag Wieers <dag@wieers.com> - 7.0.1-1
- Initial package. (using DAR)


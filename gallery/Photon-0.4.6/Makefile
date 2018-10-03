all: setup.py
	python setup.py build

clean: setup.py
	python setup.py clean
	rm -rf build dist
	rm -f Photon/*.pyc
	rm -rf debian/python2.3-photon*
	rm -rf debian/python2.4-photon*
	rm -rf debian/photon debian/files

install: setup.py
	python setup.py install --home=~

dist: setup.py
	python setup.py sdist --formats=gztar,bztar,zip

rpm: setup.py
	python setup.py bdist_rpm

deb: setup.py
	version=`./photon --version | cut -f2 -d " "` ; \
		echo "photon ($$version-1) unstable; urgency=low" > debian/changelog
	echo "" >> debian/changelog
	echo "  * New upstream release" >> debian/changelog
	echo "" >> debian/changelog
	echo " -- Luc Saillard <luc@saillard.org>  `date -R`" >> debian/changelog
	dpkg-buildpackage -rfakeroot


.PHONY: all clean install dist rpm

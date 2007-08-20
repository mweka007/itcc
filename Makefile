PYTHON?=python2.4

all: build-python2.5 build-python2.4
	$(PYTHON) setup.py build bdist_egg
debug: clean
	$(PYTHON) setup.py build --debug
	$(PYTHON) setup.py install
install: install-python2.5 install-python2.4

install-python2.5: build-python2.5

build-python2.5:
	python2.5 setup.py build --build-lib

install2:
	mkdir -p $(HOME)/public_html/
	for file in dist/*.egg; do \
		cp $$file $(HOME)/public_html/; \
		ip=$(shell python -c "import socket; print socket.gethostbyaddr(socket.gethostname())[-1][0]"); \
		echo http://$$ip/~$(USER)/$$(basename $$file); \
	done

install3:
	sudo svn-clean
	$(PYTHON) ./setup.py bdist
	sudo $(PYTHON) `which easy_install` dist/*.egg

dist: sdist
sdist:
	$(PYTHON) setup.py sdist -f
bdist:
	$(PYTHON) setup.py bdist
clean:
	rm -rf build dist MANIFEST itcc/__init__.py subdirs itcc.egg-info
	-find . -name *.pyc -exec rm -f {} \;
	-find . -name *.o -exec rm -f {} \;
	-find . -name *.so -exec rm -f {} \;
check:
	python setup.py test

deb:
	DH_ALWAYS_EXCLUDE=.svn debuild

help:
	@echo "you can use following commands:"
	@echo " make; sudo make install"
	@echo " make dist"
	@echo " make bdist"
	@echo " make deb"

TAGS:
	rm -f TAGS
	find ./ -name "*.c" -type f -exec etags -a {} \;
	find ./ -name "*.py" -type f -exec etags -a {} \;

.PHONY: TAGS test clean deb

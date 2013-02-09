pypycore
========

gevent.core implemented as cffi module, might be used with pypy (someday)

Installation
============
	pip install git+git://github.com/schmir/gevent@pypy-hacks
	pip install cffi
	git clone https://github.com/schmir/pypycore.git pypycore
	cd pypycore
	CFLAGS=-O2 pip install -e .
	export GEVENT_LOOP=pypycore.loop

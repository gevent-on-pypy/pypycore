pypycore
========

gevent.core implemented as cffi module, might be used with pypy (someday)

Installation
============

	pip install cffi
	git clone https://github.com/schmir/pypycore.git pypycore
	cd pypycore
	pip install -e .
	export GEVENT_LOOP=pypycore.loop

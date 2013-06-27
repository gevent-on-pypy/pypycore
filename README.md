pypycore
========

gevent.core implemented as cffi module, might be used with pypy (someday)

Installation
============
	pip install git+git://github.com/schmir/gevent@pypy-hacks
	pip install cffi
	pip install git+git://github.com/gevent-on-pypy/pypycore
	export GEVENT_LOOP=pypycore.loop

pypycore
========

gevent.core implemented as cffi module, might be used with pypy (someday)

Installation
============

Make sure you have PyPy 2.0 or greater (must also work with CPython 2.7).
Gevent and pypycore must be installed were PyPy will be able to find them,
and virtualenv can be used such environment:

	$ virtualenv -p /path/to/bin/pypy venv
	$ source venv/bin/activate
	(venv)$ pip install git+git://github.com/schmir/gevent@pypy-hacks
	(venv)$ pip install cffi
	(venv)$ pip install git+git://github.com/gevent-on-pypy/pypycore
	(venv)$ export GEVENT_LOOP=pypycore.loop

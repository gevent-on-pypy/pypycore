#! /usr/bin/env python

from distutils.core import setup

# you must import at least the module(s) that define the ffi's
# that you use in your application
import pypycore

setup(name="pypycore",
      version="0.1",
      py_modules=["pypycore"],
      ext_modules=[pypycore.ffi.verifier.get_extension()],
      packages=["gevent"],
      package_dir={"gevent": "gevent"},
      package_data={"gevent": ["libev.h"]})

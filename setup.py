#!/usr/bin/env python
#
# This file is part of pdfparser.
#
# pdfparse is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pdfparser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pdfparser.  If not, see <http://www.gnu.org/licenses/>.
#
# Original version by Ivan Zderadicka  (https://github.com/izderadicka/pdfparser)
# Adopted and modified by Rossum (https://github.com/rossumai/pdfparser)

from __future__ import print_function

import os
import subprocess

from setuptools import Extension, setup

try:
    from Cython.Build import cythonize
except ImportError:
    import sys
    print('You need to install cython first - sudo pip install cython', file=sys.stderr)
    sys.exit(1)


# https://gist.github.com/smidm/ff4a2c079fed97a92e9518bd3fa4797c
def pkgconfig(*packages, **kw):
    """
    Query pkg-config for library compile and linking options. Return configuration in distutils
    Extension format.

    Usage:

    pkgconfig('opencv')

    pkgconfig('opencv', 'libavformat')

    pkgconfig('opencv', optional='--static')

    pkgconfig('opencv', config=c)

    returns e.g.

    {'extra_compile_args': [],
     'extra_link_args': [],
     'include_dirs': ['/usr/include/ffmpeg'],
     'libraries': ['avformat'],
     'library_dirs': []}

     Intended use:

     distutils.core.Extension('pyextension', sources=['source.cpp'], **c)

     Set PKG_CONFIG_PATH environment variable for nonstandard library locations.

    based on work of Micah Dowty (http://code.activestate.com/recipes/502261-python-distutils-pkg-config/)
    """
    config = kw.setdefault('config', {})
    optional_args = kw.setdefault('optional', '')

    flag_map = {'include_dirs': ['--cflags-only-I', 2],
                'library_dirs': ['--libs-only-L', 2],
                'libraries': ['--libs-only-l', 2],
                'extra_compile_args': ['--cflags-only-other', 0],
                'extra_link_args': ['--libs-only-other', 0]}

    for package in packages:
        for distutils_key, (pkg_option, n) in flag_map.items():
            items = subprocess.check_output(['pkg-config', optional_args, pkg_option, package]).decode('utf8').split()
            config.setdefault(distutils_key, []).extend([i[n:] for i in items])

    return dict((k, list(set(v))) for k, v in config.items())


# If a directory containing both poppler and pycairo is given by POPPLER_CAIRO_ROOT
# they will be used, otherwise it is assumed both poppler and cairo are available
# in form of distribution-based packages.
POPPLER_CAIRO_ROOT = os.environ.get('POPPLER_CAIRO_ROOT', None)

if POPPLER_CAIRO_ROOT:
    append_root = lambda path: os.path.join(POPPLER_CAIRO_ROOT, path)

    package_data = {'pdfparser': ['*.so.*']}
    poppler_cairo_config = {'extra_compile_args': ["-std=c++11"],
                            'include_dirs': list(map(append_root, ['poppler', 'poppler/poppler', 'pycairo/cairo/'])),
                            'library_dirs': list(map(append_root, ['poppler', 'poppler/glib'])),
                            'libraries': ['poppler', 'poppler-glib'],
                            'runtime_library_dirs': ['$ORIGIN']}

    for k, v in pkgconfig('cairo').items():
        poppler_cairo_config.setdefault(k, []).extend(v)
else:
    package_data = {}
    # Still fails on a variation of this: pdfparser/poppler.cpp:602:29: fatal error:
    # CairoFontEngine.h: No such file or directory, I do not think there is a package
    # that installs the needed cairo-specific headers.
    poppler_cairo_config = pkgconfig('poppler', 'poppler-glib', 'pycairo', 'cairo')

setup(name='pdfparser-rossum',
      version='1.1.0',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Topic :: Text Processing',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'],
      description="python bindings for poppler",
      long_description="Binding for libpoppler with a focus on fast text extraction from PDF documents and rendering into cairo.",
      keywords='poppler pdf parsing rendering mining extracting',
      url='https://github.com/rossumai/pdfparser',
      install_requires=['cython'],
      packages=['pdfparser'],
      package_data=package_data,
      include_package_data=True,
      zip_safe=False,
      ext_modules=cythonize(Extension('pdfparser.poppler',
                                      ['pdfparser/poppler.pyx'],
                                      language='c++',
                                      **poppler_cairo_config)))

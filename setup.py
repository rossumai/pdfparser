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
import sys

from setuptools import Extension, setup

# cython is used only for sdist, then let's use the compiled .cpp file
try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False


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


def link_pycairo_header():
    """
    # When pycairo is installed via pip rather than apt, it's header pycairo.h or
    # py3cairo.h in location like /usr/local/lib/python2.7/dist-packages/cairo/include
    # rather than /usr/include/pycairo for python-cairo-dev and pkg-config cannot find it.
    # Thus we have to add the path by hand.
    # See also: https://github.com/pygobject/pycairo/pull/96/files
    #
    # In addition the Python2/3 header file name differs: pycairo.h vs py3cairo.h.
    # The Cython code depends on one name and cannot change it dynamically.
    # As a hack we symlink the original header to a local file with constant name.
    """
    import cairo

    source_dir = cairo.get_include()
    # Since Cython source depends on pycairo.h and cannot make it conditional,
    # let's copy the file locally to the same name for any Python as a workaround.
    source_file = 'py3cairo.h' if sys.version_info[0] == 3 else 'pycairo.h'
    source_path = os.path.join(source_dir, source_file)
    target_dir = 'pycairo'
    target_path = os.path.join(target_dir, 'pycairo.h')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if os.path.exists(target_path):
        os.unlink(target_path)
    os.symlink(source_path, target_path)
    return target_dir


def make_ext_modules():
    # https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compilation
    link_pycairo_header()
    pycairo_pc = 'py3cairo' if sys.version_info[0] == 3 else 'pycairo'
    ext_config = pkgconfig('poppler', 'poppler-glib', pycairo_pc, 'cairo')
    ext_config['include_dirs'] += ['pycairo/']
    ext_config['extra_compile_args'] = ["-std=c++11"]

    file_ext = 'pyx' if USE_CYTHON else 'cpp'

    extensions = [Extension('pdfparser.poppler',
                            ['pdfparser/poppler.{}'.format(file_ext)],
                            language='c++',
                            **ext_config)]
    if USE_CYTHON:
        extensions = cythonize(extensions)
    return extensions


setup(name='pdfparser-rossum',
      version='1.3.2',
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
      install_requires=['pycairo>=0.16.0'],
      packages=['pdfparser'],
      include_package_data=True,
      zip_safe=False,
      ext_modules=make_ext_modules())

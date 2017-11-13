#!/usr/bin/env python
#
# This file is part of pdfparser.
#
# pdfparse is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
# Original version by Ivan Zderadicka  (https://github.com/izderadicka/pdfparser)
# Adopted and modified by Rossum (https://github.com/rossumai/pdfparser)

from __future__ import print_function

from setuptools import Extension, setup

try:
    from Cython.Build import cythonize
except ImportError:
    import sys
    print('You need to install cython first - sudo pip install cython', file=sys.stderr)
    sys.exit(1)

poppler_ext = Extension('pdfparser.poppler', ['pdfparser/poppler.pyx'], language='c++',
                        extra_compile_args=["-std=c++11"],
                        include_dirs=['poppler', 'poppler/poppler', 'pycairo/cairo/', '/usr/include/cairo',
                                      '/usr/include/freetype2'],
                        library_dirs=['poppler', 'poppler/glib'],
                        libraries=['poppler', 'poppler-glib'],
                        runtime_library_dirs=['$ORIGIN'])

package_data = {'pdfparser': ['*.so.*']}

setup(name='pdfparser',
      version='0.1.1',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: PDF Parsing',

          'License :: OSI Approved :: GPLv3',

          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      description="python bindings for poppler",
      long_description="Binding for libpoppler with a focus on fast text extraction from PDF documents.",
      keywords='poppler pdf parsing mining extracting',
      url='https://github.com/izderadicka/pdfparser',
      install_requires=['cython'],
      packages=['pdfparser'],
      package_data=package_data,
      include_package_data=True,
      ext_modules=cythonize(poppler_ext),
      zip_safe=False
      )

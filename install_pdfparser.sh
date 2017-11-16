#!/bin/sh
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

sudo apt-get update
sudo apt-get install -y libtool pkg-config gettext fontconfig libfontconfig1-dev autoconf libzip-dev libtiff5-dev libopenjpeg-dev

pip install -r requirements.txt

# This would be ideal way to install pdfparser but some cairo-specific headers
# are just not included in any of poppler related packages
# sudo apt-get install -y libpoppler-dev libpoppler-private-dev libpoppler-glib-dev python-cairo-dev
# python setup.py install

sudo apt-get install -y libcairo2 libcairo2-dev
git clone --depth 1 --branch poppler-0.61.1 https://anongit.freedesktop.org/git/poppler/poppler.git
git clone --depth 1 --branch v1.15.4 https://github.com/pygobject/pycairo.git

cd poppler
cmake -DCMAKE_BUILD_TYPE=release -DENABLE_CPP=OFF -DENABLE_GLIB=ON -DENABLE_QT4=OFF -DENABLE_QT5=OFF  -DBUILD_GTK_TESTS=OFF -DENABLE_SPLASH=OFF -DENABLE_UTILS=OFF
make

cp libpoppler.so.?? ../pdfparser/
cp glib/libpoppler-glib.so.? ../pdfparser/

cd ../pycairo
python setup.py install
cd ..

POPPLER_CAIRO_ROOT='.' python setup.py install

# build a source and binary package
POPPLER_CAIRO_ROOT='.' python setup.py sdist
POPPLER_CAIRO_ROOT='.' python setup.py bdist_wheel
# can be installed with: pip install dist/*.whl
# publishing:
# $ pip install twine
### test PyPI:
# twine upload twine upload --repository-url https://test.pypi.org/legacy/ dist/*
### test install:
# pip install --verbose --index-url https://test.pypi.org/simple/ pdfparser
### production PyPI;
# twine upload twine upload dist/*

rm -rf poppler pycairo

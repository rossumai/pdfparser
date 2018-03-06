#!/bin/bash
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

set -e

# install without sudo while inside virtualenv
need_sudo=`python -c 'import sys; print(not hasattr(sys, "real_prefix") and (not hasattr(sys, "base_prefix") or sys.prefix == sys.base_prefix))'`

sudo apt-get install -y pkg-config libfontconfig1 libzip4 libtiff5 libopenjpeg5

if [[ ${need_sudo} == 'True' ]]; then sudo pip install -r requirements.txt; else pip install -r requirements.txt; fi

# This would be ideal way to install pdfparser but some cairo-specific headers
# are just not included in any of poppler related packages
# sudo apt-get install -y libpoppler-dev libpoppler-private-dev libpoppler-glib-dev python-cairo-dev
# python setup.py install

sudo apt-get install -y libcairo2 libcairo2-dev
git clone --depth 1 --branch v1.15.4 https://github.com/pygobject/pycairo.git

cp poppler/libpoppler.so.?? pdfparser/
cp poppler/glib/libpoppler-glib.so.? pdfparser/

cd pycairo
if [[ ${need_sudo} == 'True' ]]; then sudo python setup.py install; else python setup.py install; fi
cd ..

if [[ ${need_sudo} == 'True' ]]
then
    sudo POPPLER_CAIRO_ROOT='.' python setup.py install
    # build a source and binary package
    sudo POPPLER_CAIRO_ROOT='.' python setup.py sdist
    sudo POPPLER_CAIRO_ROOT='.' python setup.py bdist_wheel
    sudo rm -rf build dist pdfparser.egg-info
else
    POPPLER_CAIRO_ROOT='.' python setup.py install
    # build a source and binary package
    POPPLER_CAIRO_ROOT='.' python setup.py sdist
    POPPLER_CAIRO_ROOT='.' python setup.py bdist_wheel
    rm -rf build dist pdfparser.egg-info
fi

# can be installed with: pip install dist/*.whl
# publishing:
# $ pip install twine
### test PyPI:
# twine upload twine upload --repository-url https://test.pypi.org/legacy/ dist/*
### test install:
# pip install --verbose --index-url https://test.pypi.org/simple/ pdfparser
### production PyPI;
# twine upload twine upload dist/*

if [[ ${need_sudo} == 'True' ]]
then
    sudo rm -rf poppler pycairo
else
    rm -rf poppler pycairo
fi

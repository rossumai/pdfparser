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
#
# Original version by Ivan Zderadicka  (https://github.com/izderadicka/pdfparser)
# Adopted and modified by Rossum (https://github.com/rossumai/pdfparser)
#
# A part of this code was inspired by vistafonts-installer
# (http://plasmasturm.org/code/vistafonts-installer/). vistafonts-installer
# is a free software distributed under the terms of MIT License.
# For more information about the license see the attached original
# vistafonts-installer script.

set -e

# install without sudo while inside virtualenv
need_sudo=`python -c 'import sys; print(not hasattr(sys, "real_prefix") and (not hasattr(sys, "base_prefix") or sys.prefix == sys.base_prefix))'`

sudo apt-get update
sudo apt-get install -y cmake libtool pkg-config gettext fontconfig libfontconfig1-dev autoconf libzip-dev libtiff5-dev libopenjpeg-dev cabextract

MS_FONTS_ARCHIVE=IELPKTH.CAB
MS_FONTS_DIR=/usr/share/fonts/truetype/msttcorefonts/

VISTA_FONTS_ARCHIVE=PowerPointViewer.exe
VISTA_FONTS_DIR=/usr/share/fonts/truetype/vistafonts/

TMPDIR=`mktemp -d`
trap 'rm -rf $TMPDIR $MS_FONTS_ARCHIVE $VISTA_FONTS_ARCHIVE' EXIT INT QUIT TERM

sudo apt install ttf-mscorefonts-installer
wget https://sourceforge.net/projects/corefonts/files/OldFiles/$MS_FONTS_ARCHIVE
cabextract -L -F 'tahoma*ttf' -d $TMPDIR $MS_FONTS_ARCHIVE
sudo mv $TMPDIR/tahoma* $MS_FONTS_DIR
sudo chmod 600 $MS_FONTS_DIR/tahoma*
sudo fc-cache -fv $MS_FONTS_DIR

wget http://download.microsoft.com/download/f/5/a/f5a3df76-d856-4a61-a6bd-722f52a5be26/$VISTA_FONTS_ARCHIVE
cabextract -L -F ppviewer.cab -d $TMPDIR $VISTA_FONTS_ARCHIVE

sudo cabextract -L -F '*.TT[FC]' -d $VISTA_FONTS_DIR $TMPDIR/ppviewer.cab

( cd $VISTA_FONTS_DIR && sudo mv cambria.ttc cambria.ttf && sudo chmod 600 \
        calibri{,b,i,z}.ttf cambria{,b,i,z}.ttf candara{,b,i,z}.ttf \
        consola{,b,i,z}.ttf constan{,b,i,z}.ttf corbel{,b,i,z}.ttf )

fc-cache -fv $VISTA_FONTS_DIR

if [[ ${need_sudo} == 'True' ]]; then sudo pip install -r requirements.txt; else pip install -r requirements.txt; fi

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

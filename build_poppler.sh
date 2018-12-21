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

set -e

apt-get install -y coreutils git gcc g++ cmake make libtool pkg-config gettext libfontconfig1-dev autoconf libzip-dev libtiff5-dev libcairo2-dev
git clone --depth 1 --branch poppler-0.61.1 https://anongit.freedesktop.org/git/poppler/poppler.git
cd poppler
cmake -DCMAKE_BUILD_TYPE=release -DENABLE_CPP=OFF -DENABLE_GLIB=ON -DENABLE_QT4=OFF -DENABLE_QT5=OFF  -DBUILD_GTK_TESTS=OFF -DENABLE_SPLASH=OFF -DENABLE_UTILS=OFF
make
chown --recursive $SUDO_UID: .

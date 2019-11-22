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
# A part of this code was inspired by vistafonts-installer
# (http://plasmasturm.org/code/vistafonts-installer/). vistafonts-installer
# is a free software distributed under the terms of MIT License.
# For more information about the license see the attached original
# vistafonts-installer script.

set -e

apt-get install -y cabextract coreutils debconf fontconfig wget

MS_FONTS_ARCHIVE=IELPKTH.CAB
MS_FONTS_DIR=/usr/share/fonts/truetype/msttcorefonts/

VISTA_FONTS_ARCHIVE=PowerPointViewer.exe
VISTA_FONTS_DIR=/usr/share/fonts/truetype/vistafonts/

TMPDIR=`mktemp -d`
trap 'rm -rf $TMPDIR' EXIT INT QUIT TERM
cd "$TMPDIR"

echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections
apt-get install -y ttf-mscorefonts-installer

wget https://sourceforge.net/projects/corefonts/files/OldFiles/$MS_FONTS_ARCHIVE

if cabextract -L -F 'tahoma*ttf' -d $MS_FONTS_DIR  $MS_FONTS_ARCHIVE
then
    chmod 644 $MS_FONTS_DIR/tahoma*
    fc-cache -fv $MS_FONTS_DIR
else
    echo "ERROR: Failed to install Tahoma font!"
    exit 1
fi

wget https://sourceforge.net/projects/mscorefonts2/files/cabs/$VISTA_FONTS_ARCHIVE

if cabextract -L -F ppviewer.cab $VISTA_FONTS_ARCHIVE
then
    cabextract -L -F '*.TT[FC]' -d $VISTA_FONTS_DIR ppviewer.cab

    ( cd $VISTA_FONTS_DIR && mv cambria.ttc cambria.ttf && chmod 644 \
            calibri{,b,i,z}.ttf cambria{,b,i,z}.ttf candara{,b,i,z}.ttf \
            consola{,b,i,z}.ttf constan{,b,i,z}.ttf corbel{,b,i,z}.ttf )
    fc-cache -fv $VISTA_FONTS_DIR
else
    echo "ERROR: Failed to install Vista fonts!"
    exit 1
fi

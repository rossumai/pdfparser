#!/bin/sh
# Copyright (c) 2007-2018 Aristotle Pagaltzis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

set -e

die() { exec 2>&1 ; for line ; do echo "$line" ; done ; exit 1 ; }
exists() { which "$1" &> /dev/null ; }

[ -d ~/.fonts ] || die \
	'There is no .fonts directory in your home.' \
	'Is fontconfig set up for privately installed fonts?'

ARCHIVE=PowerPointViewer.exe
URL="https://sourceforge.net/projects/mscorefonts2/files/cabs/$ARCHIVE"

if ! [ -e "$ARCHIVE" ] ; then
	if   exists curl  ; then curl -A '' -LO      "$URL"
	elif exists wget  ; then wget -U ''          "$URL"
	elif exists fetch ; then fetch --user-agent= "$URL"
	else die 'You have neither curl nor wget nor fetch.' \
		'Please manually download this file first:' "$URL"
	fi
fi

TMPDIR=`mktemp -d`
trap 'rm -rf "$TMPDIR"' EXIT INT QUIT TERM

cabextract -L -F ppviewer.cab -d "$TMPDIR" "$ARCHIVE"

cabextract -L -F '*.TT[FC]' -d ~/.fonts "$TMPDIR/ppviewer.cab"

( cd ~/.fonts && mv cambria.ttc cambria.ttf && chmod 600 \
	calibri{,b,i,z}.ttf cambria{,b,i,z}.ttf candara{,b,i,z}.ttf \
	consola{,b,i,z}.ttf constan{,b,i,z}.ttf corbel{,b,i,z}.ttf )

fc-cache -fv ~/.fonts

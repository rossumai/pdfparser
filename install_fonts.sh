#!/bin/bash
# Installs pre-packaged msttcorefonts + vistafonts, because originals
# are not available anymore (see install_fonts_orig.sh).

set -e

apt-get install -y fontconfig wget

TMPDIR=`mktemp -d`
trap 'rm -rf $TMPDIR' EXIT INT QUIT TERM
cd "$TMPDIR"

wget http://rossum.install.s3-website-eu-west-1.amazonaws.com/msfonts.tar.gz

FONTS_DIR=/usr/share/fonts/truetype
mkdir -p ${FONTS_DIR}
tar -xzf msfonts.tar.gz -C ${FONTS_DIR}
fc-cache -fv ${FONTS_DIR}/{msttcore,vista}fonts/

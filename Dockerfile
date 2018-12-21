# --build-arg UBUNTU_VERSION=16.04 or 18.04
ARG UBUNTU_VERSION=
FROM ubuntu:${UBUNTU_VERSION}

# Ideally we'd install pdfparser via the following commands, but some
# cairo-specific headers are just not included in any of poppler related packages
# so we have to compile everything ourselves.
#
# sudo apt-get install -y libpoppler-dev libpoppler-private-dev \
#   libpoppler-glib-dev python-cairo-dev
# python setup.py install

RUN apt-get update \
    && apt-get install -y \
        autoconf \
        cmake \
        coreutils \
        g++ \
        gcc \
        gettext \
        git \
        libcairo2 \
        libcairo2-dev \
        libfontconfig1 \
        libfontconfig1-dev \
        libopenjp2-7 \
        libopenjp2-7-dev \
        libtiff5 \
        libtiff5-dev \
        libtool \
        libzip-dev \
        libzip4 \
        make \
        pkg-config \
        python-dev \
        python-pip \
        python3-dev \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# install poppler
RUN git clone --depth 1 --branch poppler-0.61.1 \
        https://anongit.freedesktop.org/git/poppler/poppler.git \
    && cd poppler \
    && cmake -DCMAKE_BUILD_TYPE=release -DENABLE_CPP=OFF -DENABLE_GLIB=ON \
        -DENABLE_QT4=OFF -DENABLE_QT5=OFF -DBUILD_GTK_TESTS=OFF \
        -DENABLE_SPLASH=OFF -DENABLE_UTILS=OFF \
    && make

# install pycairo
RUN git clone --depth 1 --branch v1.15.4 \
        https://github.com/pygobject/pycairo.git \
    && cd pycairo \
    && python setup.py install \
    && python3 setup.py install

# build pdfparser
WORKDIR /build/pdfparser

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt \
    && pip3 install -r requirements.txt

COPY . ./
RUN cp /build/poppler/libpoppler.so.?? \
        /build/poppler/glib/libpoppler-glib.so.? \
        pdfparser/ \
    && POPPLER_CAIRO_ROOT='/build' python setup.py sdist \
    && POPPLER_CAIRO_ROOT='/build' python setup.py bdist_wheel \
    && POPPLER_CAIRO_ROOT='/build' python3 setup.py bdist_wheel

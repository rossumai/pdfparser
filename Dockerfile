# --build-arg UBUNTU_VERSION=16.04 or 18.04
ARG UBUNTU_VERSION=
FROM ubuntu:${UBUNTU_VERSION}

RUN apt update \
    && apt install -y software-properties-common \
    && LC_ALL=C.UTF-8 add-apt-repository -y -u ppa:bzamecnik/poppler \
    && apt install -y \
        libcairo2-dev>=1.14.8 \
        libpoppler-dev libpoppler-private-dev libpoppler-glib-dev \
        python-dev \
        python-pip \
        python3-dev \
        python3-pip \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /pdfparser

COPY requirements.txt requirements-src.txt ./
RUN pip install -r requirements.txt \
    && pip3 install -r requirements.txt \
    && pip install --no-binary :all: -r requirements-src.txt \
    && pip3 install --no-binary :all: -r requirements-src.txt

COPY . ./
RUN python setup.py sdist

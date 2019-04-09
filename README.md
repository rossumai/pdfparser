pdfparser
---------

Python binding for `libpoppler` - focused on text extraction from PDF documents.

Intended as an easy to use replacement for [pdfminer](https://github.com/euske/pdfminer),
which provides much better performance (see below for short comparison) and is Python3 compatible.
This packages is based on [izderadicka/pdfparser](https://github.com/izderadicka/pdfparser)
and almost completely rewritten, so the package name changed to
`pdfparser-rossum` to avoid conflicting builds.

See this [article](http://zderadicka.eu/parsing-pdf-for-fun-and-profit-indeed-in-python/)
for some comparisons with pdfminer and other approaches.

Binding is written in [cython](http://cython.org/).

Requires recent `libpoppler` >= 0.40 - so I'd recommend to build it from source to get latest library,
but it works also with recent `libpoppler` library present in common linux distributions (then it requires
dev package to build). See below for installation instructions.

Available under GPL v3 or any later version license (`libpoppler` is also GPL).

## How to install

Below or some instructions to install this package. Better use Docker build.

```
git clone --depth 1 https://github.com/rossumai/pdfparser.git
cd pdfparser
sudo ./install_fonts.sh
sudo ./build_poppler.sh
sudo apt-get install -y coreutils g++ gcc git libcairo2 libcairo2-dev libfontconfig1 libopenjpeg5 libtiff5 libzip4 pkg-config python-dev
# If not in virtualenv, run install_pdfparser.sh with sudo
./install_pdfparser.sh
#test that it works
python tests/dump_file.py test_docs/test1.pdf
```

## Building with Docker

Make sure the proper version is set at `setup.py`. Ideally build the final
releases from `master` branch.

Example:

```bash
VERSION=1.2.0
docker build --build-arg UBUNTU_VERSION=16.04 -t pdfparser:${VERSION}-16.04 .
```

The build artifacts are inside the image in `/build/pdfparser/dist/`.

You can build the packages for Ubuntu 16.04/18.04 and Python 2/3 via a script:

```bash
./build_all_packages.sh 1.2.0
```

The resulting artifacts will be located at host machine at
`artifacts/{16.04,18.04}/*`. The wheels for Ubutnu 18.04 will have version with
suffix, eg. `1.2.0_bionic`.

NOTE: we packages some `.so` files from Poppler and they depend on a particular
version of Ubuntu.

## Publishing

```bash
# for example
twine upload -r myrepo artifacts/16.04/*
# publish sources only once (for 16.04)
twine upload -r myrepo artifacts/18.04/*.whl
```

Then tag the repo.

## Installing

```
# Ubuntu Xenial - latest version
pip install pdfparser-rossum
# Ubuntu Bionic - version has a specific and has to be explicit
pip install pdfparser-rossum==1.2.0-bionic
```

## Speed comparisons

|                             | pdfreader     | pdfminer      |speed-up factor|
| --------------------------- | ------------- | ------------- |---------------|
| tiny document (half page)   | 0.033s        | 0.121s        | 3.6 x         |
| small document (5 pages)    | 0.141s        | 0.810s        | 5.7 x         |
| medium document (55 pages)  | 1.166s        | 10.524s       | 9.0 x         |       
| large document (436 pages)  | 10.581s       | 108.095s      | 10.2 x        |


pdfparser code used in test

    import pdfparser.poppler as pdf
    import sys

    d=pdf.PopplerDocument(sys.argv[1])

    print('No of pages', d.no_of_pages)
    for p in d:
        print('Page', p.page_no, 'size =', p.size)
        for f in p:
            print(' '*1,'Flow')
            for b in f:
                print(' '*2,'Block', 'bbox=', b.bbox.as_tuple())
                for l in b:
                    print(' '*3, l.text.encode('UTF-8'), '(%0.2f, %0.2f, %0.2f, %0.2f)'% l.bbox.as_tuple())
                    #assert l.char_fonts.comp_ratio < 1.0
                    for i in range(len(l.text)):
                        print(l.text[i].encode('UTF-8'), '(%0.2f, %0.2f, %0.2f, %0.2f)'% l.char_bboxes[i].as_tuple(),\
                            l.char_fonts[i].name, l.char_fonts[i].size, l.char_fonts[i].color,)
                    print()

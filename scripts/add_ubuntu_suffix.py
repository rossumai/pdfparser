#!/usr/bin/env python
"""
Rename files adding version suffix specific to given version of Ubuntu.

```
scripts/add_ubuntu_suffix.py -s bionic artifacts/18.04/*.whl
```

```
# eg. it renames
pdfparser_rossum-1.2.0-cp27-cp27mu-linux_x86_64.whl
# to
pdfparser_rossum-1.2.0_bionic-cp27-cp27mu-linux_x86_64.whl
"""
from __future__ import print_function, division
import argparse
import os
import shutil


def add_ubuntu_suffix(fname, suffix):
    if suffix:
        parts = fname.split('-')
        if not parts[1].endswith(suffix):
            parts[1] += '_' + suffix
        return '-'.join(parts)
    else:
        return fname


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--suffix', required=True)
    parser.add_argument('paths', nargs='+')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    for old_name in args.paths:
        new_name = add_ubuntu_suffix(old_name, args.suffix)
        if old_name != new_name:
            print('Renaming', old_name, 'to', new_name)
            shutil.move(old_name, new_name)

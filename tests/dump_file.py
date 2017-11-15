#!/usr/bin/env python

import pdfparser.poppler as pdf
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help='document filename')
    parser.add_argument('--chars', action='store_true',
                        help='print character details')
    parser.add_argument('-f', '--first-page', type=int, default=1,
                        help='the page to start parsing from')
    parser.add_argument('-l', '--last-page', type=int,
                        help='the page to stop parsing at')
    parser.add_argument('--physical-layout', action='store_true',
                        help='maintain (as best as possible) the original physical layout of the text')
    parser.add_argument('--fixed-pitch', type=float, default=0.0,
                        help='assume fixed-pitch (or tabular) text, with the specified character width (in points).')
    args = parser.parse_args()

    document = pdf.PopplerDocument(args.filename, args.physical_layout, args.fixed_pitch)

    first_page = (args.first_page - 1) or 0
    last_page = args.last_page or (document.page_count() - 1)

    print 'Number of pages:', document.page_count()
    for page in document:
        if page.page_number < first_page or page.page_number > last_page:
            continue
        print 'Page', page.page_number, 'size = ', page.size
        for flow in page:
            print ' ' * 1, 'Flow'
            for block in flow:
                print ' ' * 2, 'Block', '(bbox: %0.2f, %0.2f, %0.2f, %0.2f)' % block.bbox.as_tuple()
                for line in block:
                    print ' ' * 3, 'Line', line.text.encode('UTF-8'), '(bbox: %0.2f, %0.2f, %0.2f, %0.2f)' % line.bbox.as_tuple()
                    if args.chars:
                        for i in range(len(line.text)):
                            print ' ' * 4, line.text[i].encode('UTF-8'), '(bbox: %0.2f, %0.2f, %0.2f, %0.2f)' % line.char_bboxes[i].as_tuple(), line.char_fonts[i].name, line.char_fonts[i].size, line.char_fonts[i].color


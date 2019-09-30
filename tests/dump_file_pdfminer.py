#!/usr/bin/env python
from __future__ import print_function

import argparse

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox,LTChar, LTFigure
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage


class PdfMinerWrapper(object):
    """
    Usage:
    with PdfMinerWrapper('2009t.pdf') as doc:
        for page in doc.get_pages():
    """
    def __init__(self, pdf_doc, pdf_pwd=""):
        self.pdf_doc = pdf_doc
        self.pdf_pwd = pdf_pwd

    def __enter__(self):
        #open the pdf file
        self.fp = open(self.pdf_doc, 'rb')
        # create a parser object associated with the file object
        parser = PDFParser(self.fp)
        # create a PDFDocument object that stores the document structure
        doc = PDFDocument(parser, password=self.pdf_pwd)
        # connect the parser and document objects
        parser.set_document(doc)
        self.doc=doc
        return self

    def _parse_pages(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams(char_margin=3.5, all_texts = True)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(self.doc):
            interpreter.process_page(page)
            # receive the LTPage object for this page
            layout = device.get_result()
            # layout is an LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
            yield layout

    def __iter__(self):
        return iter(self._parse_pages())

    def __exit__(self, _type, value, traceback):
        self.fp.close()


if __name__=='__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('filename',
                        help='document filename')
    parser.add_argument('--chars', action='store_true',
                        help='print character details')
    parser.add_argument('-f', '--first-page', type=int, default=1,
                        help='the page to start parsing from')
    parser.add_argument('-l', '--last-page', type=int,
                        help='the page to stop parsing at')
    args = parser.parse_args()

    with PdfMinerWrapper(args.filename) as document:
        first_page = (args.first_page - 1) or 0
        last_page = args.last_page or 1000000

        for page in document:
            if page.pageid < first_page or page.pageid > last_page:
                continue
            print('Page', page.pageid, 'size = ', (page.height, page.width))
            for tbox in page:
                if not isinstance(tbox, LTTextBox):
                    continue
                print(' ' * 1, 'Block', '(bbox: %0.2f, %0.2f, %0.2f, %0.2f)' % tbox.bbox)
                for obj in tbox:
                    print(' ' * 2, 'Line', obj.get_text().encode('UTF-8')[:-1], '(bbox: %0.2f, %0.2f, %0.2f, %0.2f)' % tbox.bbox)
                    if args.chars:
                        for c in obj:
                            if not isinstance(c, LTChar):
                                continue
                            print(' ' * 3, c.get_text().encode('UTF-8'), '(bbox: %0.2f, %0.2f, %0.2f, %0.2f)' % c.bbox, c.fontname.split('+')[-1], c.size)

#!/usr/bin/env python
from __future__ import print_function

import os.path

import psutil

import pdfparser.poppler as pdf


def get_total_memory():
    """
    Returns the total amount of virtual memory used by the process.
    """
    return psutil.Process().memory_info().vms


start_vm = get_total_memory()

for i in range(10000):
    i_start_vm = get_total_memory()

    document = pdf.PopplerDocument(os.path.join(os.path.dirname(__file__), '../test_docs/test1.pdf'))
    document_info = document.page_count()
    for page in document:
        page_info = page.page_number, page.size
        for flow in page:
            for block in flow:
                block_info = block.bbox.as_tuple()
                for line in block:
                    line_info = line.text.encode('UTF-8'), line.bbox.as_tuple()
                    for c in range(len(line.text)):
                        char_info = line.text[c].encode('UTF-8'), line.char_bboxes[c].as_tuple(), line.char_fonts[c].name, line.char_fonts[c].size, line.char_fonts[c].color

    i_end_vm = get_total_memory()

    # Have memory consumption increased
    if (i_end_vm - i_start_vm) > 0:
        print('iteration: %d,' % i)
        print('memory: %d' % get_total_memory(), 'increase %d' % (i_end_vm - i_start_vm))

end_vm = get_total_memory()

print("Memory consumed in total: %d" % (end_vm - start_vm))

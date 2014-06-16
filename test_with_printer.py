# -*- coding: utf-8 -*-

import traceback
from printing_tools import print_file, print_text

try:
	print print_file("test_with_printer.py")
except Exception as err:
	traceback.print_exc()
	print err

try:
	print print_text("Sample text!")
except Exception as err:
	traceback.print_exc()
	print err
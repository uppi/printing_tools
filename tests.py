import unittest, printing_tools
printing_tools.IS_UNIT_TEST = True

class TestUnix(unittest.TestCase):
	def test_list(self):
		printers = printing_tools.list_printers()
		self.assertNotEqual(printers, [])
		self.assertEqual(printers, ['Canon_MG3500_series'])

	def test_print_text(self):
		self.assertEqual(['lpr'], printing_tools.print_text("Sample Text"))
		self.assertEqual(['lpr', '-Pololo'], printing_tools.print_text("Sample Text", printer_name="ololo"))

	def test_print_file(self):
		with self.assertRaises(printing_tools.PrintError):
			printing_tools.print_file("azaza")
		self.assertEqual(['lpr', '-Pololo', 'tests.py'], printing_tools.print_file("tests.py", printer_name="ololo"))


if __name__ == '__main__':
    unittest.main()
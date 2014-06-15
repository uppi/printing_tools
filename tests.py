import unittest, printing_tools
printing_tools.IS_UNIT_TEST = True

if printing_tools.IS_WIN:
    class TestWin(unittest.TestCase):
        def test_list(self):
            printers = printing_tools.printers()
            self.assertIn('Canon MG3500 series Printer', printers)

        def test_print_text(self):
            self.assertEqual(True, printing_tools.print_text("Sample Text"))
            self.assertEqual(False, printing_tools.print_text("Sample Text", printer_name="ololo"))

        def test_print_file(self):
            with self.assertRaises(printing_tools.PrintError):
                printing_tools.print_file("azaza")
            self.assertEqual([0, 'print', 'tests.py', '/d:"ololo"', '.', 0], 
                printing_tools.print_file("tests.py", printer_name="ololo"))

else:
    class TestUnix(unittest.TestCase):
        def test_list(self):
            printers = printing_tools.printers()
            self.assertIn('Canon_MG3500_series', printers)

        def test_print_text(self):
            self.assertEqual(['lpr'], printing_tools.print_text("Sample Text"))
            self.assertEqual(['lpr', '-Pololo'], printing_tools.print_text("Sample Text", printer_name="ololo"))

        def test_print_file(self):
            with self.assertRaises(printing_tools.PrintError):
                printing_tools.print_file("azaza")
            self.assertEqual(['lpr', '-Pololo', 'tests.py'], printing_tools.print_file("tests.py", printer_name="ololo"))


if __name__ == '__main__':
    unittest.main()
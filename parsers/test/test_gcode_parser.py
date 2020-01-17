import unittest

from io import StringIO

from parsers.gcode_parser import GcodeParser

class Testing(unittest.TestCase):
    def setUp(self):
        self.testline = "; test"
        file_in = StringIO()
        file_out = StringIO()
        file_in.write(self.testline+"\n")
        file_in.seek(0)

        self.parser = GcodeParser(file_in, file_out)

    def test_parse_line(self):
        self.parser.parse()
        self.assertEqual(self.parser.linecount_in, 1)
        self.assertEqual(self.parser.current_line, self.testline)

    def test_write_line(self):
        self.parser.write_line(self.testline)

        self.parser.file_out.seek(0)
        written_line = self.parser.file_out.readline().strip()

        self.assertEqual(self.parser.linecount_out, 1)
        self.assertEqual(self.testline, written_line)

if __name__ == '__main__':
    unittest.main()

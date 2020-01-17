from parsers.gcode_parser import GcodeParser

class GcodeCopy(GcodeParser):
    def parse_line(self, line):
        self.write_line(line)

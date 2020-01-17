from parsers.gcode_parser import GcodeParser

class GcodeStrip(GcodeParser):
    def parse_line(self, line):
        parts = line.split(";")
        maybeCode = parts[0].strip()
        if maybeCode:
            self.write_line(maybeCode)

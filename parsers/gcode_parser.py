import logging

class GcodeParser(object):
    def __init__(self, file_in, file_out):
        self.file_in = file_in
        self.file_out = file_out
        self.linecount_in = 0
        self.linecount_out = 0
        self.current_line = ""

    def __get_file_name(self,file_object):
        if hasattr(file_object, "name"):
            return file_object.name
        else:
            return "<noname>"

    def parse(self):
        file_in_name = self.__get_file_name(self.file_in)
        file_out_name = self.__get_file_name(self.file_out)
        logging.info ("Parsing gcode file {}".format(file_in_name))
        for line in self.file_in:
            self.linecount_in+=1
            self.current_line = line.strip()
            self.__parse_line(line.strip())
        logging.info ("Finished parsing {} lines from {}".format(self.linecount_in, file_in_name))
        logging.info ("Finished writing {} lines to {}".format(self.linecount_out, file_out_name))

    def __parse_line(self,line):
        logging.debug ("Parsing line #{} > {} ".format(self.linecount_in,line))
        self.parse_line(line)

    def parse_line(self,line):
        pass

    def write_line(self,line):
        self.linecount_out +=1
        logging.debug ("Writing line #{} > {} ".format(self.linecount_out,line))
        print(line, file=self.file_out)

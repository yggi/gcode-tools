import logging

class GcodeParser(object):
    def __init__(self, file_in, file_out):
        self.file_in = file_in
        self.file_out = file_out
        self.linecount_in = 0
        self.linecount_out = 0


    def parse(self):
        #with open(self.filepathIn, "r") as fileIn:
        logging.info ("Parsing gcode file {}".format(self.file_in.name))
        for line in self.file_in:
            self.linecount_in+=1
            self.__parse_line(line.strip())
        logging.info ("Finished parsing {} lines from {}".format(self.linecount_in, self.file_in.name))

        #self.fileOut.close()
        logging.info ("Finished writing {} lines to {}".format(self.linecount_out, self.file_out.name))

    def __parse_line(self,line):
        logging.debug ("Parsing line #{} > {} ".format(self.linecount_in,line))
        self.parse_line(line)

    def parse_line(self,line):
        pass

    def write_line(self,line):
        self.linecount_out +=1
        logging.debug ("Writing line #{} > {} ".format(self.linecount_out,line))
        print(line, file=self.file_out)

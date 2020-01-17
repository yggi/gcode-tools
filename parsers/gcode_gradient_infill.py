# This functionality was adapted from GradientInfill by CNC Kitchen
# https://github.com/CNCKitchen/GradientInfill

import logging
import re

from typing import List, Tuple

from parsers.gcode_parser import GcodeParser
from utility import geometry

class GcodeGradientInfill(GcodeParser):
    def __init__(self, flow_max, flow_min, width, *args, **kwargs):
        self.last_position = self.current_position = (-100000,-100000)
        self.current_section = "StartLayer"
        self.perimeter_segments = []
        self.current_segment = None
        self.flow_max = flow_max
        self.flow_min = flow_min
        self.gradient_width = width

        super().__init__(*args, **kwargs)

    def get_extrusion_multiplier(self,distance):
        r = self.flow_max+distance*(self.flow_min-self.flow_max)/self.gradient_width
        return max(r,self.flow_min)

    def get_position(self,line):
        searchX = re.search(r"X(\d*\.?\d*)", line)
        searchY = re.search(r"Y(\d*\.?\d*)", line)
        if searchX and searchY:
            elementX = searchX.group(1)
            elementY = searchY.group(1)
        else:
            raise SyntaxError('Gcode file parsing error for line {line}')
        return (float(elementX), float(elementY))

    def is_layerchange(self,line):
        return "; move to next layer" in line

    def is_begin_innerwall(self,line):
        return not self.perimeter_segments and "; move to first perimeter point" in line

    def is_end_innerwall(self,line):
        return self.perimeter_segments and "; move to first perimeter point" in line

    def is_move(self,line):
        return " X" in line and " Y" in line and ("G1" in line or "G0" in line)

    def is_innerwall_perimeter(self,line):
        return self.current_section == "InnerWall" and "; perimeter" in line

    def is_infill(self,line):
        return line.endswith("; infill")

    def min_perimeter_distance(self,segment):
        center = ((segment[0][0] + segment[1][0]) / 2, (segment[0][1] + segment[1][1]) / 2)
        return min(geometry.distance_line_to_point(s,center) for s in self.perimeter_segments)

    def modify_infill(self,line):
        stripped_line = line.split(";")[0]

        #only valid for short segments
        dist = self.min_perimeter_distance(self.current_segment)

        extrusion_factor = self.get_extrusion_multiplier(dist)
        # Example : G1 X62.416 Y68.522 E0.02980
        regex= r"^(?P<G>\w+)\sX(?P<X>\d*\.\d*)\sY(?P<Y>\d*\.\d*)\sE(?P<E>\d*\.\d*)"
        matches= re.search(regex, stripped_line)

        g = matches.group("G")
        x = matches.group("X")
        y = matches.group("Y")
        e = float(matches.group("E"))

        e_new = e * extrusion_factor

        newline = "{} X{} Y{} E{:.5f}".format(g,x,y,e_new)
        return newline + "; E_old={:.5f} mindist={:.2f} E_factor={:.2f}  ; infill".format(e, dist, extrusion_factor)


    def parse_line(self, line):
        logging.debug("Current Section : {}".format(self.current_section))

        # Update position
        if self.is_move(line):
            self.last_position = self.current_position
            self.current_position = self.get_position(line)
            self.current_segment = (self.last_position, self.current_position)

        # check for and handle different sections
        if self.is_layerchange(line):
            self.current_section = "StartLayer"
            self.perimeter_segments = []

        elif self.is_begin_innerwall(line):
            self.current_section = "InnerWall"

        elif self.is_innerwall_perimeter(line):
            self.perimeter_segments.append(self.current_segment)

        elif self.is_end_innerwall(line):
            self.current_section = "Nothing"

        elif self.is_infill(line):
            new_line = self.modify_infill(line)
            self.write_line(new_line)
            return

        self.write_line(line)

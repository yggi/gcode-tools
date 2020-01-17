#!/usr/bin/env python3

"""
Gcode manipulation tools
"""

import logging
import argparse
import sys

from parsers.gcode_strip import GcodeStrip
from parsers.gcode_gradient_infill import GcodeGradientInfill

def main():
    """ Parse arguments, sets up logging, run selected gcode parser."""

    # Command line arguments
    parser = argparse.ArgumentParser(
        prog="gct.py",
        description="Tools to parse and manipulate gcode"
    )

    parser.add_argument(
        "--file_out",
        "-f",
        #"outfile",
        type=argparse.FileType('w+'),
        nargs='?',
        help="Path to the output gcode file",
        default=sys.stdout
    )

    parser.add_argument(
        '-d', '--debug',
        help="be very verbose",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )

    parser.add_argument(
        '-v', '--verbose',
        help="be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )

    subprasers = parser.add_subparsers(dest='command', required=True)

    # TODO: this should be an optional argument and default to stdin
    # but setting nargs='?' breaks parsing if FILE_IN is provided.
    parser.add_argument(
        "file_in",
        type=argparse.FileType('r'),
        #nargs='?',
        help="Path to the input gcode file",
        default=sys.stdin
    )

    # 'strip' command
    strip = subprasers.add_parser('strip', help='strip comments')

    # 'gradient_infill' command
    gradient = subprasers.add_parser('gradient_infill', help='modify infill to gradient')

    gradient.add_argument(
        "--flow_min",
        type=float,
        required=False,
        default=0.5,
        help="minimum extrusion flow multiplier, default 0.5",
    )

    gradient.add_argument(
        "--flow_max",
        type=float,
        required=False,
        default=3.0,
        help="maximum extrusion flow multiplier, default 3.0",
    )

    gradient.add_argument(
        "--width",
        type=float,
        required=False,
        default=5.0,
        help="width of the extrusion gradient in mm from closest perimeter. Default 5.0",
    )
    args = parser.parse_args()

    # Logging
    logging.basicConfig(format='%(asctime)s %(message)s', level=args.loglevel)


    # Select and run the appropriate gcode parser
    gcode_parser = None

    gcode_parser_args = {
        "file_out": args.file_out,
        "file_in": args.file_in
    }

    if args.command == "strip":
        gcode_parser = GcodeStrip(**gcode_parser_args)

    elif args.command == "gradient_infill":
        gcode_parser = GcodeGradientInfill(
            flow_min=args.flow_min,
            flow_max=args.flow_max,
            width=args.width,
            **gcode_parser_args
        )

    gcode_parser.parse()

if __name__ == '__main__':
    main()

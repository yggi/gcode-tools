# Gcode Tools

A collection of G-code postprocessing tools. Mostly for 3D-Printing.

This software is in an early development stage. Things might break.

## General Usage

```
gct.py [-o FILE_OUT] COMMAND ... FILE_IN
```

If no `FILE_OUT` is given, output is written to stdout.

Commands may have command-specific parameters.

Check `gct.py -h` for more information.

## Available Tools

### Strip

Removes all comments from a gcode file. This is a minimal parser for development, but may be useful on its own.

#### Usage

```
gct.py strip FILE_IN
```

### Gradient Infill

Changes the amount of extrusion depending on the distance to the closest perimeter. This functionality was adapted from [GradientInfill by CNC Kitchen](https://github.com/CNCKitchen/GradientInfill). Many thanks to Stefan for his great work!

#### Usage

```
gct.py gradient_infill [--flow_min FLOW_MIN] [--flow_max FLOW_MAX]  [--width WIDTH] FILE_IN
```
Check `gct.py gradient_infill -h` for more information.

#### Notes

* Currently `gradient_infill` probably only works with gcode created by [PrusaSlicer](https://www.prusa3d.com/prusaslicer/).
* Currently only works with infill consisting of small line segments.
* `Print Settings -> Output options -> Verbose G-code` must be enabled.
* `Printer Settings -> General -> Use relative E distances ` must be enabled.
* On printers with bowden extruder, reduce the speed for the infill.

## License
Released under the MIT License.

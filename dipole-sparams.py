#!/usr/bin/env python

from scipy.special import sici
from math import log, cos, sin, pi, log10
import argparse
from tabulate import tabulate

eta = 119.9169832*pi
euler = 0.5772156649

def dipoleImpedance( frequency, length, diameter ):
  radius = diameter/2
  k = 2*pi*frequency/299792458

  resistance_m = (eta/(2*pi))*(euler + log(k*length) - sici(k*length)[1] + 0.5*sin(k*length)*(sici(2*k*length)[0] - 2*sici(k*length)[0]) + 0.5*cos(k*length)*(euler + log(k*length/2) + sici(2*k*length)[1] - 2*sici(k*length)[1]))

  resistance = resistance_m / (sin(k*length/2)*sin(k*length/2))

  reactance_m = (eta/(4*pi))*(2*sici(k*length)[0] + cos(k*length)*(2*sici(k*length)[0] - sici(2*k*length)[0]) - sin(k*length)*(2*sici(k*length)[1] - sici(2*k*length)[1] - sici(2*k*radius*radius/length)[1]))

  reactance = reactance_m / (sin(k*length/2)*sin(k*length/2))

  impedance = complex(resistance, reactance)
  return impedance

def ZtoS11( z, z0 ):
  s11 = (z - z0) / (z + z0)
  return s11

parser = argparse.ArgumentParser()
parser.add_argument("-f1", type=float, help="Lower frequency (MHz)")
parser.add_argument("-f2", type=float, help="Upper frequency (MHz) (optional)")
parser.add_argument("-l", type=float, help="Dipole length (m)")
parser.add_argument("-d", type=float, help="Wire diameter (mm)")
parser.add_argument("-p", type=int, help="Number of points to sweep, minimum 1")
parser.add_argument("-o", type=argparse.FileType('w', 0), help="Filename for Touchstone output (optional)")
parser.add_argument("--skip-output", dest="skipoutput", help="Skip printing the table of values", action="store_true")

args = parser.parse_args()

frequency1 = 0
frequency2 = 0
length = 0
diameter = 0
points = 0

print("\nWire dipole antenna S-parameter calculator")
print("Written by Peter Kazakoff, University of Victoria")
print("\nBased on eqns 8-60a, 8-60b, 8-61a, and 8-61b from \n\"Antenna Theory, 3rd ed.\" by Constantine A. Balanis")
print("\nThis program is BSD licensed and comes with ABSOLUTELY NO WARRANTY\n\n")

if args.f1 > 0:
  frequency1 = args.f1*1E6
else:
  exit("E: lower frequency must be specified\n")

if args.f2 > 0:
  frequency2 = args.f2*1E6
else:
  frequency2 = frequency1

if args.l > 0:
  length = args.l
else:
  exit("E: length must be a real number greater than zero\n")

if args.d > 0:
  diameter = args.d*0.001
else:
  exit("E: wire diameter must be greater than zero\n")

if args.p >= 1:
  points = args.p
else:
  exit("E: number of points must be greater than or equal to 1\n")

sparamTable = []
tsOut = []

if (args.skipoutput and (args.o is None)):
  print("E: When specifying --skip-output, you must specify a touchstone file with -o\n")
  parser.print_help()

for i in range(0, points):
  freqPoint = frequency1 + i*(frequency2-frequency1)/points
  impedance = dipoleImpedance(freqPoint, length, diameter)
  s11 = ZtoS11(impedance, 50.0)
  s11_db = 20*log10(abs(s11))
  sparamTable.append(["{0:.2f}".format(freqPoint/1E6), impedance.real, impedance.imag, s11_db, s11])
  tsOut.append(["{:5f}".format(freqPoint/1E6), "{:15.13f}".format(s11.real), "{:15.13f}".format(s11.imag)])

if not args.skipoutput:
  print tabulate(sparamTable, headers=["Frequency (MHz)", "R (ohms)", "X (j*ohms)", "|S11| (db)", "S11"]) + "\n"

if args.o is not None:
  #args.o.write('! Dipole antenna return loss \n' + '! Frequency: ' + {0:.2f}.format(frequency1/1E6)  + ' to ' + {0:.2f}.format(frequency2/1E6) + ' MHz, ' + str(points) + 'steps.\n ! L=' + {0:.2f}.format(length) + 'm, d=' + {0:.2f}.format(diameter*1000) + 'mm\n')
  args.o.write('# MHz S RI R 50 \n\n')
  for datapoint in tsOut:
    args.o.write( datapoint[0] + ' ' + datapoint[1] + ' ' +  datapoint[2] + "\n" )
  print("Wrote Touchstone File " + args.o.name)

print("\n")

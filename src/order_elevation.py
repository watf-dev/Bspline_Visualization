#!/usr/bin/env python3
# Created: May, 07, 2025 09:48:57 by Wataru Fukuda
import os
import sys
import numpy

class OrderElevation():
  def __init__(self, order, cxyz):
    self.order = order
    self.cxyz = cxyz
    self.ns = len(cxyz)//self.order
    self.split()
    self.update_cxyz()

  def split(self):
    self.segments = []
    print("self.ns",self.ns)
    for s in range(self.ns):
      tmp = []
      for i in range(self.order+1):
        tmp.append(self.cxyz[(self.order-1)*s+i])  # todo
        # tmp.append(self.cxyz[(self.order)*s+i])  # todo
      self.segments.append(tmp)

  def update_cxyz(self):
    self.cxyz_new = [] 
    for s,seg in enumerate(self.segments):
      for i in range(self.order+2):
        print("s",s,"i",i)
        alpha = i/(self.order+1)
        if i == 0:
          cxyz_tmp = (1-alpha)*seg[i]
        elif i == self.order +1:
          cxyz_tmp = alpha*seg[i-1]
        else:
          cxyz_tmp = (1-alpha)*seg[i] + alpha*seg[i-1]
        if i == self.order + 1 and self.ns != 1:
          if s != 0:
            print("nested")
            print(cxyz_tmp)
            self.cxyz_new.append(cxyz_tmp)
        else:
          print("symple")
          print(cxyz_tmp)
          self.cxyz_new.append(cxyz_tmp)
    self.cxyz_new = numpy.array(self.cxyz_new, dtype='>f8')

def main():
  import argparse
  parser = argparse.ArgumentParser(description="""\

""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("cxyz", help="control point data")
  parser.add_argument("-t", "--txt", action='store_true', help="import cxyz as txt")
  parser.add_argument("--nsd", type=int, default=3, help="number of spatial dimension")
  parser.add_argument("--order", type=int, default=2, help="order now")
  parser.add_argument("-o", "--output", metavar="output-file", default=None, help="output file")
  parser.add_argument("--debug", action='store_true', help="debug mode")
  options = parser.parse_args()

  if options.txt:
    cxyz = numpy.loadtxt(options.cxyz, dtype='>f8')
  else:
    cxyz = numpy.fromfile(options.cxyz, dtype='>f8').reshape(-1, options.nsd)
  if options.debug:
    print(cxyz)

  OE = OrderElevation(order=options.order, cxyz=cxyz)
  if options.output:
    # OE.cxyz_new.tofile(options.output)
    numpy.savetxt(os.path.join("OUTPUT","GLOBAL","xyz_final.txt"),OE.cxyz_new)
  else:
    print(OE.cxyz_new)

if __name__ == '__main__':
  main()


#!/usr/bin/env python3
# Created: Oct, 31, 2024 23:59:05 by Wataru Fukuda

def main():
  import argparse
  parser=argparse.ArgumentParser(description="""\
make knots vector
""")
  parser.add_argument("-p","--order",metavar="polynomial-order",default=2,help="polynomial order")
  parser.add_argument("-e","--element",metavar="element-number",default=4,help="element number")
  parser.add_argument("-o","--output",metavar="output-file",default="knots",help="output file")
  parser.add_argument("--output_dir",metavar="output-dir",default="OUTPUT",help="output dir")
  options=parser.parse_args()

  import numpy
  import os

  order = int(options.order)
  ele = int(options.element)
  arr_ = []
  for i in range(ele+1):
    if (i == 0) or (i == ele):
      for _ in range(order+1):
        arr_.append(i)
    else:
      arr_.append(i)
  kv=numpy.array(arr_, dtype=">f8")

  os.makedirs(options.output_dir,exist_ok=True)
  kv.tofile(os.path.join(options.output_dir,options.output))


if(__name__=='__main__'):
  main()


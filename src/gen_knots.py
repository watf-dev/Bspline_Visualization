#!/usr/bin/env python3
# Created: Oct, 31, 2024 23:59:05 by Wataru Fukuda

def main():
  import argparse
  parser=argparse.ArgumentParser(description="""\
make knots vector
""")
  parser.add_argument("-o","--output",metavar="output-file",default="knots",help="output file")
  parser.add_argument("--output_dir",metavar="output-dir",default="OUTPUT",help="output dir")
  options=parser.parse_args()

  import numpy
  import os

  kv=numpy.array([0,0,0,1,2,3,4,4,4],dtype=">f8")
  # kv=numpy.array([0,0,0,0,1,2,3,4,4,4,4],dtype=">f8")
  os.makedirs(options.output_dir,exist_ok=True)
  kv.tofile(os.path.join(options.output_dir,options.output))


if(__name__=='__main__'):
  main()


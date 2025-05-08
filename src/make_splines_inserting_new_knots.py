#!/usr/bin/env python3
# Created: Oct, 31, 2024 23:58:10 by Wataru Fukuda
import os
import numpy
from scipy.special import comb

def recursiveBspline(i,p,x,knots):
  if p == 0:
    return numpy.where((knots[i] <= x) & (x < knots[i+1]), 1.0, 0.0)
  else:
    left = 0.0
    if knots[i+p] != knots[i]:
      left = ((x-knots[i])/(knots[i+p]-knots[i]))*recursiveBspline(i,p-1,x,knots)
    right = 0.0
    if knots[i+p+1] != knots[i+1]:
      right = ((knots[i+p+1]-x)/(knots[i+p+1]-knots[i+1]))*recursiveBspline(i+1,p-1,x,knots)
    return left + right

def insertKnots(kv,p,xi,k):
  nn=kv.size-p-1
  K=numpy.zeros((nn,nn+1),dtype=">f8")
  # print("bf insertion",kv)
  # print("to be inserted",xi)
  # print("idx",k)
  for a in range(nn+1):
    if 0<=a<=k-p-1:
      alpha=1.0
    # elif k-p<=a<=k:  # todo
    elif k-p<=a<=k-1:
      alpha=(xi-kv[a])/(kv[a+p]-kv[a])
    # elif k+1<=a<=nn+1:  # todo
    elif k<=a<=nn:
      alpha=0.0
    if a==0:
      K[a,a]=alpha
    elif a==nn:
      K[a-1,a]=1-alpha
    else:
      K[a-1,a]=1-alpha
      K[a,a]=alpha
  kv=numpy.insert(kv,k,xi)
  return K,kv

def rearrangeList(_l):
  _l=numpy.array(_l)
  insertedComponents=_l[1:-1]
  for c in insertedComponents:
    _l=numpy.insert(_l,numpy.searchsorted(_l,c),c)
  return _l.reshape(-1,2)

class BernsteinPolynomials:
  def __init__(self,p):
    self.p=p
  def getValues(self,xi):
    B=numpy.zeros(self.p+1,dtype=">f8")
    for a in range(self.p+1):
      B[a]=comb(self.p,a)*2**(-self.p)*(1+xi)**a*(1-xi)**(self.p-a)
    return B

class Bspline:
  def __init__(self,kv,p):
    self.kv=kv
    self.p=p
    self.nn=kv.size-p-1  # num of N
    self.ne=numpy.unique(kv).size-1  # num of elements
    self.eBoundaries=numpy.unique(kv,return_counts=True)[0]
    self.eCounts=numpy.unique(kv,return_counts=True)[1]
    self.BP=BernsteinPolynomials(p)
    self.ien=[]
    _C=genC(kv,p)
    _C=numpy.round(_C,2)
    basisSpan=[]
    for A in range(self.nn):
      spans=numpy.unique(kv[A:A+p+2])
      spans_=kv[A:A+p+p]
      basisSpan.append(rearrangeList(spans))
    self.C=[]
    elementSpan=[]
    for e in range(self.ne):
      elementSpan=self.eBoundaries[e:e+2]
      ien=[]
      for i,bs in enumerate(basisSpan):
        for s in bs:
          if numpy.linalg.norm(s-elementSpan)<10e-08:
            ien.append(i)
      self.C.append(_C[ien[0]:ien[-1]+1,e*p:e*p+(p+1)])
      self.ien.append(numpy.array(ien,dtype=">i4"))
  def getValues(self,Xi):
    N=numpy.zeros(self.nn,dtype=">f8")
    for e in range(self.ne):
      if self.eBoundaries[e]<=Xi<=self.eBoundaries[e+1]:
        xi=2*Xi/(self.eBoundaries[e+1]-self.eBoundaries[e]) - (self.eBoundaries[e+1]+self.eBoundaries[e])/(self.eBoundaries[e+1]-self.eBoundaries[e])
        N[self.ien[e][0]:self.ien[e][-1]+1]=numpy.dot(self.C[e],self.BP.getValues(xi))
        return N

def genC(kv,p):
  nn=kv.size-p-1  # num of N
  eBoundaries,c=numpy.unique(kv,return_counts=True)
  bKnots=numpy.repeat(eBoundaries,p)
  bKnots=numpy.insert(bKnots,0,eBoundaries[0])
  bKnots=numpy.insert(bKnots,-1,eBoundaries[-1])
  _,C=numpy.unique(bKnots,return_counts=True)
  knots=[]
  for i,_c in enumerate(C-c):
    knots.extend([eBoundaries[i]]*_c)
  knots=numpy.array(knots,dtype=">f8")
  C=numpy.eye(nn,dtype=">f8")
  # print("knots",knots)
  os.makedirs(os.path.join("OUTPUT","GLOBAL","recursiveBspline0"),exist_ok=True)
  x_vals = numpy.linspace(kv[0], kv[-1], 1000)
  # for i in range(nn):
  #   y_vals = numpy.array([recursiveBspline(i, p, x, kv) for x in x_vals])
  #   mask = y_vals != 0.0
  #   numpy.savetxt(os.path.join("OUTPUT","GLOBAL","recursiveBspline0","recursiveBspline{0:1d}.txt".format(i)),numpy.stack([x_vals[mask],y_vals[mask]],axis=-1))
  for j,xi in enumerate(knots):
    nn+=1
    k=numpy.searchsorted(kv,xi)
    K,kv=insertKnots(kv,p,xi,k)
    C=numpy.dot(C,K)
    # x_vals = numpy.linspace(kv[0], kv[-1], 1000)
    # os.makedirs(os.path.join("OUTPUT","GLOBAL","recursiveBspline{0:1d}".format(j+1)),exist_ok=True)
    # for i in range(nn):
    #   y_vals = numpy.array([recursiveBspline(i, p, x, kv) for x in x_vals])
    #   mask = y_vals != 0.0
    #   numpy.savetxt(os.path.join("OUTPUT","GLOBAL","recursiveBspline{0:1d}".format(j+1),"recursiveBspline{0:1d}.txt".format(i)),numpy.stack([x_vals[mask],y_vals[mask]],axis=-1))
  return C


def main():
  import argparse
  parser=argparse.ArgumentParser(description="""\

""")
  parser.add_argument("-o","--output",default="OUTPUT",help="output directory")
  parser.add_argument("-p","--order",default=2,type=int,help="input order")
  parser.add_argument("-d","--divide",default=101,type=int,help="divide number")
  parser.add_argument("-c","--curve",help="plots data")
  parser.add_argument("file",metavar="input-file",help="input file")
  options=parser.parse_args()

  kv_init=numpy.fromfile(options.file,dtype=">f8")
  p=options.order
  div=options.divide
  if options.curve:
    xyz_init=numpy.loadtxt(options.curve)
    xyz_current = xyz_init

  kv_unique = numpy.unique(kv_init)
  kv_insert = (kv_unique[1:] + kv_unique[:-1]) / 2
  kv_insert=numpy.array(kv_insert,dtype=">f8")
  kv_list = []
  kv_list.append(kv_init)
  os.makedirs(os.path.join(options.output,"GLOBAL"),exist_ok=True)

  ### initial process ###

  ### knot insertion ###
  kv_current = kv_list[-1]
  for num, kv_in in enumerate(kv_insert):
    print("--------inserting... ",kv_in,"--------")
    kv_current = numpy.sort(numpy.append(kv_list[-1], kv_in))
    kv_list.append(kv_current)
    print("kv after inserting",kv_current)
    BS = Bspline(kv_current,p)
    for A in range(BS.nn):
      bsplines=numpy.zeros(div,dtype=">f8")
      xis=numpy.arange(0,div,dtype=">f8")*(kv_current[A+BS.p+1]-kv_current[A])/(div-1)+kv_current[A]
      for i,Xi in enumerate(xis):
        bsplines[i]=BS.getValues(Xi)[A]
      numpy.savetxt(os.path.join(options.output,"GLOBAL","N{0:1d}{1:1d}.txt".format(num,A)),numpy.stack([xis,bsplines],axis=-1))
    if options.curve:
      idx=numpy.searchsorted(kv_list[-2],kv_in)
      C,_ = insertKnots(kv_list[-2],p,kv_in,idx)
      xyz_current = numpy.dot(C.T,xyz_current)
      for i,ien_ in enumerate(BS.ien):
        xis=numpy.arange(0,div,dtype=">f8")*(BS.eBoundaries[i+1]-BS.eBoundaries[i])/(div-1)+BS.eBoundaries[i]
        xyz_e=numpy.zeros((2,div),dtype=">f8")
        for ien in ien_:
          bsplines=numpy.zeros(div,dtype=">f8")
          for j,Xi in enumerate(xis):
            bsplines[j]=BS.getValues(Xi)[ien]
          xyz_e[0,:]+=bsplines*xyz_current[ien,0]
          xyz_e[1,:]+=bsplines*xyz_current[ien,1]
        numpy.savetxt(os.path.join(options.output,"GLOBAL","curve{0:1d}{1:1d}.txt".format(num,i)),numpy.stack([xyz_e[0,:],xyz_e[1,:]],axis=-1))


if(__name__=='__main__'):
  main()


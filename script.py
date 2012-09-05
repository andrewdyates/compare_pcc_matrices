#!/usr/bin/python
"""Compute statistical significance in differences in PCC values.

EXAMPLE USES:
  python fname_pkl1=a.pkl fname_pkl2=b.pkl n1=150 n2=145 outdir=$HOME
  python multi=True fname_json=$HOME/pccs.json outdir=$HOME
"""
from __future__ import division
import numpy as np
import cPickle as pickle
import os, sys
import json


def artanh(r):
  return 0.5 * np.log((1+r)/(1-r))

def z_compare_r(r1, r2, n1, n2):
  # From http://luna.cas.usf.edu/~mbrannic/files/regression/corr1.html#correlations from 2 independent samples
  # z from normal distribution
  n = artanh(r1) - artanh(r2)
  d = np.sqrt(1/(n1-3) + 1/(n2-3))
  return n/d

def z_multi_r(rs, ns):
  # From http://luna.cas.usf.edu/~mbrannic/files/regression/corr1.html
  # q from chi-squared table
  nns = np.array(ns)-3
  zs = np.array(map(artanh, rs))
  z_hat = np.dot(nns, zs) / np.sum(nns)
  q = np.dot(nns, (zs-z_hat)**2)
  return q, z_hat

def get_outname(fname1, fname2):
  s = os.path.basepath(fname1).rpartition('.')[0]
  t = os.path.basepath(fname2).rpartition('.')[0]
  return "2pcc_ztest_%s_vs_%s.pkl" % (s, t)

def main(fname_pkl1=None, fname_pkl2=None, n1=None, n2=None, outdir=""):
  if outdir: assert os.path.exists(outdir)
  n1, n2 = int(n1), int(n2)
  assert n1 > 0 and n2 > 0 and fname_pkl1 is not None and fname_pkl2 is not None
  M1, M2 = pickle.load(open(fname_pkl1)), pickle.load(open(fname_pkl2))
  assert np.size(M1) == np.size(M2)
  Z = np.zeros(np.size(M1))
  for i in xrange(np.size(M1)):
    Z[i] = z_compare_r(r1=M1[i], n1=n1, r2=M2[i], n2=n2)

  outpath = os.path.join(outdir, get_outname(fname_pkl1, fname_pkl2))
  print "Saving results as %s." % outpath
  pickle.dump(Z, open(outpath, "w"))

def multi(fname_json=None, outdir=""):
  """Statistical test for many matrices."""
  assert fname_json is not None
  J = json.load(open(fname_json))
  Ms, ns = [], []
  size = None
  for s in J['matrices']:
    Ms.append(pickle.load(open(s['path'])))
    ns.append(s['n'])
    if size is not None:
      assert np.size(Ms[s]) == size
      size = np.size(Ms[s])
      
  Q = np.zeros(size)
  for i in xrange(size):
    v = [M[i] for M in Ms]
    Q[i] = z_multi_r(v, ns)

  outpath = os.path.join(outdir, fname_json+".all_chitest.pkl")
  print "Saving results as %s." % outpath
  pickle.dump(Q, open(outpath, "w"))
  

if __name__ == "__main__":
  argd = dict([s.split('=') for s in sys.argv[1:]])
  print argd
  if "multi" in argd:
    del argd["multi"]
    multi(**argd)
  else:
    main(**argd)

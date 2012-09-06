#!/usr/bin/python
"""Compute statistical significance in differences in PCC values.

EXAMPLE USES:

# Two matrices
# n values from: $HOME/gse15745_sept2012/gender_split_log.txt
  python $HOME/compare_pcc_matrices/script.py fname_npy1=$HOME/gse15745_sept2012/gse15745_gpl6104_female_pcc.PEARSON.values.npy fname_npy2=$HOME/gse15745_sept2012/gse15745_gpl6104_male_pcc.PEARSON.values.npy n1=184 n2=400

# Multiple matrices
  python $HOME/compare_pcc_matrices/script.py multi=True fname_json=$HOME/compare_pcc_matrices/sample.json outdir=$HOME
"""
from __future__ import division
import numpy as np
import os, sys
import json
N_REPORT=20000

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

def main(fname_npy1=None, fname_npy2=None, n1=None, n2=None, outdir=""):
  if outdir: assert os.path.exists(outdir)
  n1, n2 = int(n1), int(n2)
  assert n1 > 0 and n2 > 0 and fname_npy1 is not None and fname_npy2 is not None
  M1, M2 = np.load(fname_npy1), np.load(fname_npy2)
  assert np.size(M1) == np.size(M2)
  Z = np.zeros(np.size(M1))
  for i in xrange(np.size(M1)):
    Z[i] = z_compare_r(r1=M1[i], n1=n1, r2=M2[i], n2=n2)
    if i % N_REPORT == 0:
      print "Computed comparison %d of %d. Last value: %f" % (i, np.size(M1), Z[i])

  outpath = os.path.join(outdir, get_outname(fname_npy1, fname_npy2))
  print "Saving results as %s." % outpath
  Z.save(outpath)

def multi(fname_json=None, outdir=""):
  """Statistical test for many matrices."""
  assert fname_json is not None
  J = json.load(open(fname_json))
  Ms, ns = [], []
  size = None
  for s in J['matrices']:
    Ms.append(np.load(s['path']))
    ns.append(s['n'])
    if size is not None:
      assert np.size(Ms[-1]) == size
    size = np.size(Ms[-1])
    print "Loaded %s" % s['path']

  Q = np.zeros(size)
  for i in xrange(size):
    v = [M[i] for M in Ms]
    q, z_hat = z_multi_r(v, ns)
    Q[i] = q
    if i % N_REPORT == 0:
      print "Computed comparison %d of %d. Last value: %f" % (i, np.size(Ms[0]), Q[i])

  outpath = os.path.join(outdir, fname_json+".all_chitest.npy")
  print "Saving results as %s." % outpath
  Q.save(outpath)
  

if __name__ == "__main__":
  argd = dict([s.split('=') for s in sys.argv[1:]])
  print argd
  if "multi" in argd:
    del argd["multi"]
    multi(**argd)
  else:
    main(**argd)

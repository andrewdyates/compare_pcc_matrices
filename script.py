#!/usr/bin/python
"""Compute statistical significance in differences in PCC values.

EXAMPLE USES:

# Two matrices
# n values from: $HOME/gse15745_sept2012/gender_split_log.txt
  python $HOME/compare_pcc_matrices/script.py fname_npy1=$HOME/gse15745_sept2012/gse15745_gpl6104_female_pcc.PEARSON.values.npy fname_npy2=$HOME/gse15745_sept2012/gse15745_gpl6104_male_pcc.PEARSON.values.npy n1=184 n2=400

# Multiple matrices
  python $HOME/compare_pcc_matrices/script.py multi=True fname_json=$HOME/compare_pcc_matrices/sample.json outdir=$HOME

# Compute p-value for multi (chi statistic)
from scipy.stats import chi2
pval = 1 - chi2.cdf(q_value, dof)

# Compute p-value for gaussian pair of PCC values
from scipy.special import ndtr
pval = ndtr(z)
"""
from __future__ import division
import numpy as np
import os, sys
import json
from __init__ import *

N_REPORT=20000

def get_outname(fname1, fname2, label):
  s = os.path.basename(fname1).rpartition('.')[0]
  t = os.path.basename(fname2).rpartition('.')[0]
  return "%s_vs_%s_%s.npy" % (s, t, label)

def main(fname_npy1=None, fname_npy2=None, n1=None, n2=None, outdir=""):
  if outdir: assert os.path.exists(outdir)
  n1, n2 = int(n1), int(n2)
  assert n1 > 0 and n2 > 0 and fname_npy1 is not None and fname_npy2 is not None
  M1, M2 = np.load(fname_npy1), np.load(fname_npy2)
  assert np.size(M1) == np.size(M2)
  Z, PV = np.zeros(np.size(M1)), np.zeros(np.size(M1))
  for i in xrange(np.size(M1)):
    Z[i], PV[i] = z_compare_r(r1=M1[i], n1=n1, r2=M2[i], n2=n2)
    if i % N_REPORT == 0:
      print "Computed comparison %d of %d. Last value: %f, pv %f" % (i, np.size(M1), Z[i], PV[i])

  outpath_z = os.path.join(outdir, get_outname(fname_npy1, fname_npy2, "z"))
  outpath_pv = os.path.join(outdir, get_outname(fname_npy1, fname_npy2, "z_pv"))
  print "Saving results as %s and %s." % (outpath_z, outpath_pv)
  np.save(outpath_z, Z)
  np.save(outpath_pv, PV)

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

  Q, PV = np.zeros(size), np.zeros(size)
  for i in xrange(size):
    v = [M[i] for M in Ms]
    q, z_hat, pv = z_multi_r(v, ns)
    Q[i], PV[i] = q, pv
    if i % N_REPORT == 0:
      print "Computed comparison %d of %d. Last value: %f (pv=%f)" % (i, np.size(Ms[0]), Q[i], PV[i])

  outpath_q = os.path.join(outdir, fname_json+".all_chi.npy")
  outpath_pv = os.path.join(outdir, fname_json+".all_chi_p.npy")
  print "Saving results as %s and %s." % (outpath_q, outpath_pv)
  np.save(outpath, Q)
  np.save(outpath, PV)
  

if __name__ == "__main__":
  argd = dict([s.split('=') for s in sys.argv[1:]])
  print argd
  if "multi" in argd:
    del argd["multi"]
    multi(**argd)
  else:
    main(**argd)

#!/usr/bin/python
from __future__ import division
from scipy.stats import chi2
from scipy.special import ndtr
import numpy as np


def artanh(r):
  return 0.5 * np.log((1+r)/(1-r))

def z_compare_r(r1, r2, n1, n2):
  # From http://luna.cas.usf.edu/~mbrannic/files/regression/corr1.html#correlations from 2 independent samples
  # z from normal distribution
  n = artanh(r1) - artanh(r2)
  d = np.sqrt(1/(n1-3) + 1/(n2-3))
  z = n/d
  pv = z_to_pv(z)
  return z, pv

def z_multi_r(rs, ns):
  # From http://luna.cas.usf.edu/~mbrannic/files/regression/corr1.html
  # q from chi-squared table
  assert len(rs) == len(ns)
  nns = np.array(ns)-3
  zs = np.array(map(artanh, rs))
  z_hat = np.dot(nns, zs) / np.sum(nns)
  q = np.dot(nns, (zs-z_hat)**2)
  dof = len(rs)-1
  pv = q_to_pv(q, dof)
  return q, z_hat, pv

def q_to_pv(q, dof):
  return 1 - chi2.cdf(q, dof)

def z_to_pv(z):
  """2-sided probability."""
  return 1-abs(ndtr(z)-0.5)*2

from script import *
import unittest
import numpy as np
from StringIO import StringIO

JSON = """
{
"split_log": "test_log.txt",
"matrices": [
  {"path": "M.npy", "n": 146},
  {"path": "N.npy", "n": 146},
  {"path": "O.npy", "n": 146}
]}
"""

# Example from
#   http://luna.cas.usf.edu/~mbrannic/files/regression/corr1.html
STUDY = [
{'id': 1, 'r': .2, 'n': 200, 'z': .2, '(n-3)*z': 39.94, 'zbar': .41, '(z-zbar)^2': .0441, 'q': 8.69},
{'id': 2, 'r': .5, 'n': 150, 'z': .55, '(n-3)*z': 80.75, 'zbar': .41, '(z-zbar)^2': .0196, 'q': 2.88},
{'id': 3, 'r': .6, 'n': 75, 'z': .69, '(n-3)*z': 49.91, 'zbar': .41, '(z-zbar)^2': .0784, 'q': 5.64}
]
Q, Z_BAR = 17.21, 0.41

R1, R2, N1, N2, Z = .63, .70, 150, 175, -1.18
PV1, Z1 = 0.05/2, -1.96
PV2, Q2 = 0.05, 5.99

class TestAll(unittest.TestCase):
  def test_multi(self):
    for d in STUDY:
      self.assertEqual(d['z'], round(artanh(d['r']),2))
    q, z_bar, pv = z_multi_r([s['r'] for s in STUDY], [s['n'] for s in STUDY])
    print q, z_bar, pv
    self.assertTrue(abs(q-Q) < 0.2)
    self.assertTrue(abs(z_bar-Z_BAR) < 0.2)

  def test_pair(self):
    z, pv = z_compare_r(R1, R2, N1, N2)
    self.assertTrue(abs(z-Z) < 0.1)
    self.assertTrue(pv > 0.05)

  def test_stats(self):
    self.assertTrue(abs(q_to_pv(5.99, 2) - 0.05) < 0.01)
    print z_to_pv(-1.96)
    self.assertTrue(abs(z_to_pv(-1.96)-0.05) < 0.01)
    self.assertTrue(abs(z_to_pv(-1.96)-z_to_pv(1.96)) < 0.001)
  def test_artanh_zero(self):
    self.assertFalse(np.isnan(artanh(1)))
    self.assertFalse(np.isnan(artanh(0)))
    self.assertFalse(np.isnan(artanh(-1)))
    self.assertRaises(AssertionError, artanh, -1.5)
    self.assertRaises(AssertionError, artanh, 1.5)

def manual_test():
  M = np.array([0.5, 0.2, -0.1, 1, -1, 0, 9])
  N = np.array([-0.5, 0.1, -0.7, 1, -1, 0.3, 0.9])
  O = np.array([-0.5, 0.1, -0.7, 1, -1, 0.3, 0.9])
  np.save("M.npy", M)
  np.save("N.npy", N)
  np.save("O.npy", O)
  main(fname_npy1="M.npy", fname_npy2="N.npy", n1=100, n2=200)
  multi(fname_json=StringIO(JSON))
  os.remove("M.npy")
  os.remove("N.npy")
  os.remove("O.npy")
  os.remove("M_vs_N_z.npy")
  os.remove("M_vs_N_z_pv.npy")

  

if __name__ == "__main__":
  manual_test()
  unittest.main()

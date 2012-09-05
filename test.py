from script import *
import unittest

# Example from
#   http://luna.cas.usf.edu/~mbrannic/files/regression/corr1.html
STUDY = [
{'id': 1, 'r': .2, 'n': 200, 'z': .2, '(n-3)*z': 39.94, 'zbar': .41, '(z-zbar)^2': .0441, 'q': 8.69},
{'id': 2, 'r': .5, 'n': 150, 'z': .55, '(n-3)*z': 80.75, 'zbar': .41, '(z-zbar)^2': .0196, 'q': 2.88},
{'id': 3, 'r': .6, 'n': 75, 'z': .69, '(n-3)*z': 49.91, 'zbar': .41, '(z-zbar)^2': .0784, 'q': 5.64}
]
Q, Z_BAR = 17.21, 0.41

R1, R2, N1, N2, Z = .63, .70, 150, 175, -1.18

class TestAll(unittest.TestCase):
  def test_multi(self):
    for d in STUDY:
      self.assertEqual(d['z'], round(artanh(d['r']),2))
    q, z_bar = z_multi_r([s['r'] for s in STUDY], [s['n'] for s in STUDY])
    print q, z_bar
    self.assertLess(abs(q-Q), 0.2)
    self.assertLess(abs(z_bar-Z_BAR), 0.2)

  def test_pair(self):
    z = z_compare_r(R1, R2, N1, N2)
    self.assertLess(abs(z-Z), 0.1)
    

if __name__ == "__main__":
  unittest.main()

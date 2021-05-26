import unittest
import numpy as np
import sample.load_looks as lookc

class TestLoadLooks(unittest.TestCase):
    # Just one integration test: does it get the same answer as the R code?
    def test_load_looks(self):
      looks2 = lookc.loadCompactLooks( "data/test_save_looks")
      from_compact = lookc.formAllLooks(looks2['knockoffs'], looks2['vars_to_omit'], looks2['updates'])
      from_r = [np.genfromtxt("data/test_save_looks_full/" + str(i+1) + ".csv", skip_header = True, delimiter = ",", dtype = float) for i in range(10)]
      for k in range(len(from_r)):
        self.assertEqual( True, np.sum( np.abs( from_compact[k] - from_r[k] ) ) < 1e-10) 


if __name__ == '__main__':
    unittest.main()


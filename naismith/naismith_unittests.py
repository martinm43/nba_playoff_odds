#Working with the canonical example as a base.

import unittest 
import numpy as np
class TestSRSCalculations(unittest.TestCase):
    def test_array(self):
	a=np.asarray([4,3,1,7,9])
	b=np.asarray([4,3,1,8,9])
	for i in range(0,len(a)):
		self.assertEqual(a[i],b[i])

if __name__ == '__main__':
    unittest.main()

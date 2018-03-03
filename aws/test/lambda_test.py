import sys
import os
sys.path.append(os.path.abspath(__file__ + '/../../../../'))

import unittest

from homepi.aws.main.lambda_handler import handle_discovery_v3

class TestLambda(unittest.TestCase):

  def test_discover(self):
    response = handle_discovery_v3(None)
    self.assertGreater(len(response['event']['payload']['endpoints']), 0)

if __name__ == '__main__':
    unittest.main()


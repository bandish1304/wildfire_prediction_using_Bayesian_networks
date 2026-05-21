import unittest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Bayesian network model')))
from build_bayesian_network import model, inference

class TestBayesianNetwork(unittest.TestCase):
    def test_inference_typical(self):
        evidence = {
            'TMAX_CAT': 'High',
            'PRCP_CAT': 'Dry',
            'SEASON_weather': 'Summer'
        }
        result = inference.query(variables=['WILDFIRE_OCCURRENCE'], evidence=evidence)
        self.assertIn('WILDFIRE_OCCURRENCE', result.variables)
        self.assertTrue(hasattr(result, 'values'))
        self.assertGreaterEqual(result.values[0], 0)
        self.assertLessEqual(result.values[0], 1)

    def test_inference_missing_evidence(self):
        evidence = {
            'TMAX_CAT': 'Medium',
            'SEASON_weather': 'Spring'
        }
        result = inference.query(variables=['WILDFIRE_OCCURRENCE'], evidence=evidence)
        self.assertIn('WILDFIRE_OCCURRENCE', result.variables)
        self.assertTrue(hasattr(result, 'values'))

if __name__ == '__main__':
    unittest.main()

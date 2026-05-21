import unittest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Bayesian network model')))
from fetch_live_weather import fetch_live_weather

class TestFetchLiveWeather(unittest.TestCase):
    def test_fetch_live_weather_valid_city(self):
        # This test will only pass if you provide a valid API key in fetch_live_weather.py
        city = 'Los Angeles'
        df = fetch_live_weather(city)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('city', df.columns)
        self.assertEqual(df.iloc[0]['city'].lower(), city.lower())

    def test_fetch_live_weather_invalid_city(self):
        city = 'NotARealCity12345'
        df = fetch_live_weather(city)
        self.assertIsNone(df)

if __name__ == '__main__':
    unittest.main()

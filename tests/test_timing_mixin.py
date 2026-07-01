import unittest
import time
from io import StringIO
from unittest.mock import patch
from unittest_observability import TimingMixin

class TestTimingMixin(TimingMixin, unittest.TestCase):
    def test_short_duration(self):
        time.sleep(0.01) # Simulate a short test

    def test_long_duration(self):
        time.sleep(0.05) # Simulate a longer test

    @patch('sys.stdout', new_callable=StringIO)
    def test_output_format(self, mock_stdout):
        # Run a test to capture its output
        # We need to run a suite to trigger setUpClass/tearDownClass
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestTimingMixin))
        runner = unittest.TextTestRunner()
        runner.run(suite)

        output = mock_stdout.getvalue()
        
        # Check for class timing header
        self.assertIn("--- Timing Statistics for Test Class: TestTimingMixin ---", output)
        self.assertIn("Total Class Duration:", output)
        
        # Check for individual method timing header
        self.assertIn("Individual Method Durations (longest first):", output)

        # Check for specific method output format
        self.assertRegex(output, r"  - test_timing_mixin.TestTimingMixin.test_short_duration: \d+\.\d{4} seconds")
        self.assertRegex(output, r"  - test_timing_mixin.TestTimingMixin.test_long_duration: \d+\.\d{4} seconds")

if __name__ == '__main__':
    unittest.main()
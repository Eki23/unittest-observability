import unittest
import time
from unittest_observability.testcase.mixins.timing_mixin import TimingMixin

class TestTimingMixin(unittest.TestCase, TimingMixin): # Switched order
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # The timing_class_setup method now returns a string, but we don't need to assert it here
        cls.timing_class_setup()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        timing_stats = cls.timing_class_teardown()
        print(f"\n--- Returned Class Timing Stats for {cls.__name__} ---")
        print(timing_stats)
        print("--------------------------------------------------")
        # Assertions to check the returned data
        assert "class_name" in timing_stats
        assert "total_class_duration" in timing_stats
        assert isinstance(timing_stats["method_timings"], list)
        if timing_stats["method_timings"]:
            assert "total_methods_duration" in timing_stats

    def setUp(self):
        super().setUp()
        # The timing_method_setup method now returns a string, but we don't need to assert it here
        self.timing_method_setup()

    def tearDown(self):
        super().tearDown()
        method_stats = self.timing_method_teardown()
        print(f"Returned Method Timing Stats for {method_stats['id']}: {method_stats['duration']:.4f} seconds")
        # Assertions to check the returned data
        self.assertIn("id", method_stats)
        self.assertIn("duration", method_stats)
        self.assertIsInstance(method_stats["duration"], float)
        self.assertGreaterEqual(method_stats["duration"], 0)

    def test_short_method(self):
        time.sleep(0.05) # Simulate some work

    def test_medium_method(self):
        time.sleep(0.1) # Simulate some work

    def test_long_method(self):
        time.sleep(0.15) # Simulate some work

if __name__ == '__main__':
    unittest.main()

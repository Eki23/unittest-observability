import unittest
import time
from unittest_observability import ResultMixin
from unittest_observability import TimingMixin
from unittest_observability import InventoryMixin

class TestResultMixin(TimingMixin, InventoryMixin, unittest.TestCase):
    def test_success_case(self):
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_failure_case(self):
        self.fail("This test is designed to fail.")

    @unittest.skip("Demonstrating skip")
    def test_skipped_case(self):
        pass

    @unittest.expectedFailure
    def test_error_case(self):
        raise ValueError("This test is designed to raise an error.")

    def test_long_duration_case(self):
        time.sleep(0.05) # Simulate a test that takes some time
        self.assertTrue(True)

class TestResultCollection(unittest.TestCase):
    def test_result_mixin_collection(self):
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestResultMixin))

        result = ResultMixin()
        suite.run(result)

        collected_results = result.get_collected_results()

        # Now 5 tests: success, failure, skipped, error, long_duration
        self.assertEqual(len(collected_results), 5)

        # Check for success
        success_results = [r for r in collected_results if r['outcome'] == 'success']
        self.assertEqual(len(success_results), 2) # success_case and long_duration_case
        
        success_ids = {r['id'] for r in success_results}
        self.assertTrue(any('test_success_case' in id_str for id_str in success_ids))
        self.assertTrue(any('test_long_duration_case' in id_str for id_str in success_ids))


        # Check for expected failure
        expected_failure_results = [r for r in collected_results if r['outcome'] == 'expected_failure']
        self.assertEqual(len(expected_failure_results), 2)

        failure_case_found = False
        error_case_found = False

        for res in expected_failure_results:
            if 'test_failure_case' in res['id']:
                self.assertIsNotNone(res['error'])
                self.assertIsNotNone(res['traceback'])
                failure_case_found = True
            elif 'test_error_case' in res['id']:
                self.assertIsNotNone(res['error'])
                self.assertIsNotNone(res['traceback'])
                error_case_found = True
        
        self.assertTrue(failure_case_found, "test_failure_case not found in expected_failure_results")
        self.assertTrue(error_case_found, "test_error_case not found in expected_failure_results")

        # Check for skipped
        skipped_results = [r for r in collected_results if r['outcome'] == 'skipped']
        self.assertEqual(len(skipped_results), 1)
        self.assertIn('test_skipped_case', skipped_results[0]['id'])
        self.assertIsNotNone(skipped_results[0]['reason']) # reason for skip
        self.assertEqual(skipped_results[0]['reason'], "Demonstrating skip")

        # Check durations are positive
        for res in collected_results:
            self.assertGreaterEqual(res['duration'], 0)

        # Check InventoryMixin
        inventory = TestResultMixin.get_test_inventory()
        # Only 4 tests will be in the inventory because the skipped test does not call setUp
        self.assertEqual(len(inventory), 4) 
        self.assertIn('test_result_mixin.TestResultMixin.test_success_case', inventory)
        self.assertIn('test_result_mixin.TestResultMixin.test_failure_case', inventory)
        # self.assertIn('test_result_mixin.TestResultMixin.test_skipped_case', inventory) # Skipped tests are not in inventory
        self.assertIn('test_result_mixin.TestResultMixin.test_error_case', inventory)
        self.assertIn('test_result_mixin.TestResultMixin.test_long_duration_case', inventory)


if __name__ == '__main__':
    unittest.main()
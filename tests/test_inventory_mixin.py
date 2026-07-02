import unittest
import inspect
from unittest_observability.testcase.mixins.inventory_mixin import InventoryMixin

class TestInventoryMixin(unittest.TestCase, InventoryMixin): # Switched order
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        setup_message = cls.inventory_class_setup()
        print(f"\n--- Class Setup: {setup_message} ---")
        # Assertions for setup_message
        assert isinstance(setup_message, str)
        assert "Inventory setup for class" in setup_message

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        inventory_stats = cls.inventory_class_teardown()
        print(f"\n--- Returned Class Inventory Stats for {cls.__name__} ---")
        print(inventory_stats)
        print("--------------------------------------------------")
        # Assertions to check the returned data
        assert "class_name" in inventory_stats
        assert "total_test_methods_discovered" in inventory_stats
        assert "total_test_methods_actually_ran" in inventory_stats
        assert "total_test_methods_skipped_or_not_run" in inventory_stats
        assert isinstance(inventory_stats["skipped_or_not_run_tests"], list)
        assert isinstance(inventory_stats["all_ran_tests"], list)

        # Verify counts
        expected_count = len([name for name, method in inspect.getmembers(cls, predicate=inspect.isfunction) if name.startswith('test_')])
        assert inventory_stats["total_test_methods_discovered"] == expected_count
        assert inventory_stats["total_test_methods_actually_ran"] == 2 # test_one, test_two
        assert inventory_stats["total_test_methods_skipped_or_not_run"] == 1 # test_skipped

        # Verify skipped tests
        assert f"{cls.__module__}.{cls.__name__}.test_skipped" in inventory_stats["skipped_or_not_run_tests"]
        
        # Verify ran tests
        assert f"{cls.__module__}.{cls.__name__}.test_one" in inventory_stats["all_ran_tests"]
        assert f"{cls.__module__}.{cls.__name__}.test_two" in inventory_stats["all_ran_tests"]


    def setUp(self):
        super().setUp()
        setup_message = self.inventory_method_setup()
        print(f"--- Method Setup: {setup_message} ---")
        # Assertions for setup_message
        self.assertIsInstance(setup_message, str)
        self.assertIn("Inventory: Setting up method", setup_message)

    def tearDown(self):
        super().tearDown()
        teardown_message = self.inventory_method_teardown()
        print(f"--- Method Teardown: {teardown_message} ---")
        # Assertions for teardown_message
        self.assertIsInstance(teardown_message, str)
        self.assertIn("Inventory: Teardown complete for method", teardown_message)

    def test_one(self):
        self.assertTrue(True)

    def test_two(self):
        self.assertEqual(1, 1)

    @unittest.skip("Demonstrating a skipped test")
    def test_skipped(self):
        self.fail("This test should be skipped")

if __name__ == '__main__':
    unittest.main()

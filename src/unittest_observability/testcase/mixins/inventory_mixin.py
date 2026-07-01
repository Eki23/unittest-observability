# Copyright (c) 2026 Christian Ekiza

import unittest
import inspect

class InventoryMixin:
    """
    A mixin for unittest.TestCase to collect inventory of executed tests.
    It discovers all test methods in a class and reports on which ones ran.
    """
    _test_inventory = [] # Stores IDs of tests that actually ran
    _expected_inventory = [] # Stores IDs of all discovered test methods

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._test_inventory = [] # Clear for each test class
        cls._expected_inventory = [] # Clear for each test class

        # Discover all test methods in the class
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if name.startswith('test_'):
                # Construct the full test ID
                test_id = f"{cls.__module__}.{cls.__name__}.{name}"
                cls._expected_inventory.append(test_id)
        cls._expected_inventory.sort() # Keep it sorted for consistent reporting

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        ran_tests = set(cls._test_inventory)
        expected_tests = set(cls._expected_inventory)

        all_discovered = len(expected_tests)
        actually_ran = len(ran_tests)
        skipped_or_not_run = len(expected_tests - ran_tests)

        print(f"\n--- Inventory Statistics for Test Class: {cls.__name__} ---")
        print(f"Total Test Methods Discovered: {all_discovered}")
        print(f"Total Test Methods Actually Ran: {actually_ran}")
        
        if skipped_or_not_run > 0:
            print(f"Total Test Methods Skipped/Not Run: {skipped_or_not_run}")
            print("Skipped/Not Run Tests:")
            for test_id in sorted(list(expected_tests - ran_tests)):
                print(f"  - {test_id}")
        else:
            print("All discovered test methods were executed.")
        print("--------------------------------------------------")

    @classmethod
    def get_test_inventory(cls):
        """
        Returns a list of identifiers for all tests that have been run with this mixin.
        """
        return cls._test_inventory

    @classmethod
    def get_expected_inventory(cls):
        """
        Returns a list of identifiers for all test methods discovered in this class.
        """
        return cls._expected_inventory

    def setUp(self):
        super().setUp()
        # Collect test identification information for tests that actually start running
        test_id = self.id() # e.g., 'tests.test_my_module.TestMyClass.test_method'
        self.__class__._test_inventory.append(test_id)

    def tearDown(self):
        super().tearDown()
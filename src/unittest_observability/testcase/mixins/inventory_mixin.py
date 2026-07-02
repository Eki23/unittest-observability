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
    def inventory_class_setup(cls) -> str:
        """
        Proxy method to set up the inventory for the class.
        Should be called within the subclass's setUpClass method.
        Returns a string indicating the action and discovered tests.
        """
        # super().setUpClass() # This should be called by the actual setUpClass, not here
        cls._test_inventory = [] # Clear for each test class
        cls._expected_inventory = [] # Clear for each test class

        # Discover all test methods in the class
        for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
            if name.startswith('test_'):
                # Construct the full test ID
                test_id = f"{cls.__module__}.{cls.__name__}.{name}"
                cls._expected_inventory.append(test_id)
        cls._expected_inventory.sort() # Keep it sorted for consistent reporting
        return f"Inventory setup for class {cls.__name__}. Discovered {len(cls._expected_inventory)} expected tests."

    @classmethod
    def inventory_class_teardown(cls) -> dict:
        """
        Proxy method to finalize inventory collection for the class and return statistics.
        Should be called within the subclass's tearDownClass method.
        Returns a dictionary containing inventory statistics.
        """
        ran_tests = set(cls._test_inventory)
        expected_tests = set(cls._expected_inventory)

        all_discovered = len(expected_tests)
        actually_ran = len(ran_tests)
        skipped_or_not_run_count = len(expected_tests - ran_tests)
        skipped_or_not_run_list = sorted(list(expected_tests - ran_tests))

        stats = {
            "class_name": cls.__name__,
            "total_test_methods_discovered": all_discovered,
            "total_test_methods_actually_ran": actually_ran,
            "total_test_methods_skipped_or_not_run": skipped_or_not_run_count,
            "skipped_or_not_run_tests": skipped_or_not_run_list,
            "all_ran_tests": sorted(list(ran_tests))
        }

        # Optionally, you can still print for immediate console feedback if desired
        # print(f"\n--- Inventory Statistics for Test Class: {cls.__name__} ---")
        # print(f"Total Test Methods Discovered: {all_discovered}")
        # print(f"Total Test Methods Actually Ran: {actually_ran}")
        # if skipped_or_not_run_count > 0:
        #     print(f"Total Test Methods Skipped/Not Run: {skipped_or_not_run_count}")
        #     print("Skipped/Not Run Tests:")
        #     for test_id in skipped_or_not_run_list:
        #         print(f"  - {test_id}")
        # else:
        #     print("All discovered test methods were executed.")
        # print("--------------------------------------------------")

        return stats

    @classmethod
    def get_test_inventory(cls) -> list[str]:
        """
        Returns a list of identifiers for all tests that have been run with this mixin.
        """
        return cls._test_inventory

    @classmethod
    def get_expected_inventory(cls) -> list[str]:
        """
        Returns a list of identifiers for all test methods discovered in this class.
        """
        return cls._expected_inventory

    def inventory_method_setup(self) -> str:
        """
        Proxy method to record the start of a test method for inventory.
        Should be called within the subclass's setUp method.
        Returns a string indicating which test method is being set up.
        """
        test_id = self.id() # e.g., 'tests.test_my_module.TestMyClass.test_method'
        self.__class__._test_inventory.append(test_id)
        return f"Inventory: Setting up method {test_id}."

    def inventory_method_teardown(self) -> str:
        """
        Proxy method to finalize inventory collection for an individual test method.
        Should be called within the subclass's tearDown method.
        Returns a string indicating the action.
        """
        return f"Inventory: Teardown complete for method {self.id()}."
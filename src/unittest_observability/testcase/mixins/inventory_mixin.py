# Copyright (c) 2026 Christian Ekiza

import unittest

class InventoryMixin:
    """
    A mixin for unittest.TestCase to collect inventory of executed tests.
    """
    _test_inventory = []

    @classmethod
    def get_test_inventory(cls):
        """
        Returns a list of identifiers for all tests that have been run with this mixin.
        """
        return cls._test_inventory

    def setUp(self):
        super().setUp()
        # Collect test identification information
        test_id = self.id() # e.g., 'tests.test_my_module.TestMyClass.test_method'
        self.__class__._test_inventory.append(test_id)

    def tearDown(self):
        super().tearDown()
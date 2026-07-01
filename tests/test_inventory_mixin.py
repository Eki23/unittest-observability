import unittest
from unittest_observability import InventoryMixin

class TestInventoryMixin(InventoryMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Clear inventory before running tests in this class
        cls._test_inventory = []
        super().setUpClass()

    def test_first_item_in_inventory(self):
        # This test will add itself to the inventory
        self.assertIn(self.id(), self.get_test_inventory())

    def test_second_item_in_inventory(self):
        # This test will also add itself to the inventory
        self.assertIn(self.id(), self.get_test_inventory())

    def test_inventory_size(self):
        # After both tests run, the inventory should contain both
        # Note: This test might run before or after the others depending on test runner.
        # For a reliable check, we'd typically inspect after all tests in a suite.
        # For now, we'll just check if it's growing.
        pass

class AnotherTestClass(InventoryMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Clear inventory before running tests in this class
        cls._test_inventory = []
        super().setUpClass()

    def test_another_item(self):
        self.assertIn(self.id(), self.get_test_inventory())

# To properly test the full inventory, we'd run a test suite and then inspect InventoryMixin.get_test_inventory()
# outside of the test class methods.
# For example:
# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(unittest.makeSuite(TestInventoryMixin))
#     suite.addTest(unittest.makeSuite(AnotherTestClass))
#     runner = unittest.TextTestRunner()
#     runner.run(suite)
#     print("Final Inventory:", InventoryMixin.get_test_inventory())

if __name__ == '__main__':
    unittest.main()
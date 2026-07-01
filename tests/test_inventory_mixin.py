import unittest
import time
from io import StringIO
from unittest.mock import patch
from unittest_observability import InventoryMixin

class TestInventoryMixin(InventoryMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass() # Call mixin's setUpClass first to initialize inventories

    def test_first_item_in_inventory(self):
        self.assertIn(self.id(), self.get_test_inventory())
        self.assertIn(self.id(), self.get_expected_inventory())

    def test_second_item_in_inventory(self):
        self.assertIn(self.id(), self.get_test_inventory())
        self.assertIn(self.id(), self.get_expected_inventory())

    @unittest.skip("Demonstrating skipped test for inventory")
    def test_skipped_item(self):
        pass # This test should be in expected_inventory but not in _test_inventory

    @patch('sys.stdout', new_callable=StringIO)
    def test_inventory_reporting(self, mock_stdout):
        # This test itself will run, but we're interested in the tearDownClass output
        # To capture tearDownClass output, we need to run a suite that includes this class
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestInventoryMixin))
        runner = unittest.TextTestRunner()
        runner.run(suite)

        output = mock_stdout.getvalue()
        
        # Assertions for the tearDownClass output
        self.assertIn("--- Inventory Statistics for Test Class: TestInventoryMixin ---", output)
        self.assertIn("Total Test Methods Discovered: 4", output) # 3 actual tests + this reporting test
        self.assertIn("Total Test Methods Actually Ran: 3", output) # 3 actual tests (skipped one doesn't run)
        self.assertIn("Total Test Methods Skipped/Not Run: 1", output)
        self.assertIn("Skipped/Not Run Tests:", output)
        self.assertIn("  - test_inventory_mixin.TestInventoryMixin.test_skipped_item", output)
        self.assertIn("--------------------------------------------------", output)


class AnotherTestClass(InventoryMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass() # Call mixin's setUpClass first to initialize inventories

    def test_another_item(self):
        self.assertIn(self.id(), self.get_test_inventory())
        self.assertIn(self.id(), self.get_expected_inventory())

    @patch('sys.stdout', new_callable=StringIO)
    def test_another_reporting(self, mock_stdout):
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(AnotherTestClass))
        runner = unittest.TextTestRunner()
        runner.run(suite)

        output = mock_stdout.getvalue()
        self.assertIn("--- Inventory Statistics for Test Class: AnotherTestClass ---", output)
        self.assertIn("Total Test Methods Discovered: 2", output)
        self.assertIn("Total Test Methods Actually Ran: 2", output)
        self.assertIn("All discovered test methods were executed.", output)


if __name__ == '__main__':
    unittest.main()
# unittest-observability

This is a Python project for unittest observability.

## Features

This library provides several mixins to enhance `unittest` with observability features:

-   **`TimingMixin`**: Integrates with `unittest.TestCase` to automatically measure and report the execution time of each test method. It now uses `time.monotonic()` for more accurate duration measurements, helping in identifying slow tests and performance bottlenecks. Its proxy methods (`timing_class_setup`, `timing_class_teardown`, `timing_method_setup`, `timing_method_teardown`) now return detailed timing information or explanatory strings.
-   **`InventoryMixin`**: Designed for `unittest.TestCase`, this mixin now discovers all `test_*` methods within a class during `setUpClass`. In `tearDownClass`, it reports on the total number of tests discovered, how many actually ran, and identifies any tests that were skipped or not executed. This provides a comprehensive inventory and helps diagnose missing or skipped tests. Its proxy methods (`inventory_class_setup`, `inventory_class_teardown`, `inventory_method_setup`, `inventory_method_teardown`) now return inventory statistics or explanatory strings.
-   **`ResultMixin`**: Extends `unittest.TestResult` to gather detailed information about the outcome of each test, including success, failure, errors, skips, and execution duration. It also uses `time.monotonic()` for precise duration tracking and provides full tracebacks for issues. This provides a rich dataset for analysis and reporting.

## Usage

### `TimingMixin` and `InventoryMixin`

To use `TimingMixin` or `InventoryMixin`, simply inherit from them in your `unittest.TestCase` classes. It's recommended to place `unittest.TestCase` first in the inheritance list for conventional Method Resolution Order (MRO).

**Important:** The mixins provide *proxy methods* that must be explicitly called within your `unittest.TestCase`'s `setUpClass`, `tearDownClass`, `setUp`, and `tearDown` methods to enable their functionality. Remember to call `super().setUpClass()`/`super().setUp()` first in your setup methods, and `super().tearDownClass()`/`super().tearDown()` last in your teardown methods.

```python
import unittest
from unittest_observability import TimingMixin, InventoryMixin

class MyTests(unittest.TestCase, TimingMixin, InventoryMixin): # Updated inheritance order
    @classmethod
    def setUpClass(cls):
        super().setUpClass() # Call parent setUpClass first
        cls.inventory_class_setup() # Initialize InventoryMixin for the class
        cls.timing_class_setup()    # Initialize TimingMixin for the class

    @classmethod
    def tearDownClass(cls):
        # Call mixin teardown methods to get results before parent tearDownClass
        inventory_stats = cls.inventory_class_teardown()
        timing_stats = cls.timing_class_teardown()
        
        print(f"Class Inventory Stats: {inventory_stats}")
        print(f"Class Timing Stats: {timing_stats}")
        
        super().tearDownClass() # Call parent tearDownClass last

    def setUp(self):
        super().setUp() # Call parent setUp first
        self.inventory_method_setup() # Initialize InventoryMixin for the method
        self.timing_method_setup()    # Initialize TimingMixin for the method

    def tearDown(self):
        # Call mixin teardown methods to get results before parent tearDown
        method_inventory = self.inventory_method_teardown()
        method_timing = self.timing_method_teardown()
        
        print(f"Method Inventory: {method_inventory}")
        print(f"Method Timing: {method_timing}")
        
        super().tearDown() # Call parent tearDown last

    def test_example(self):
        # Your test code
        self.assertTrue(True)

# To access inventory (after tests have run):
# expected_inventory = MyTests.get_expected_inventory()
# ran_inventory = MyTests.get_test_inventory()
```

The proxy methods (`timing_class_setup`, `timing_class_teardown`, etc.) now return data (strings, lists, or dictionaries) which you can capture and process as needed, rather than just printing to `sys.stdout`.

### `ResultMixin`

`ResultMixin` extends `unittest.TestResult` and is designed to be used with a `unittest.TextTestRunner` (or similar test runner) by passing it as the `resultclass` argument. This allows it to collect detailed results from all tests run by the runner.

```python
import unittest
from unittest_observability import ResultMixin

# Assuming you have a TestSuite or individual TestCases
suite = unittest.TestSuite()
# suite.addTest(...)

runner = unittest.TextTestRunner(resultclass=ResultMixin)
result = runner.run(suite)

# Access collected results
detailed_results = result.get_collected_results()
for test_info in detailed_results:
    print(test_info)
```

## Development and Publishing

This project uses GitHub Actions for continuous integration and publishing. A workflow is configured to build and publish the package to TestPyPI on pushes to the `main` branch or when a new tag (e.g., `v1.0.0`) is created. The CI pipeline now also includes **coverage measurement** to ensure code quality. Ensure you have a `TEST_PYPI_API_TOKEN` GitHub Secret configured for publishing.

For local development, you can run tests with coverage using the provided batch script:
```bash
run_tests_with_coverage.bat
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes.
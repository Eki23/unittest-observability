# unittest-observability

This is a Python project for unittest observability.

## Features

This library provides several mixins to enhance `unittest` with observability features:

-   **`TimingMixin`**: Integrates with `unittest.TestCase` to automatically measure and report the execution time of each test method. It now uses `time.monotonic()` for more accurate duration measurements, helping in identifying slow tests and performance bottlenecks.
-   **`InventoryMixin`**: Designed for `unittest.TestCase`, this mixin now discovers all `test_*` methods within a class during `setUpClass`. In `tearDownClass`, it reports on the total number of tests discovered, how many actually ran, and identifies any tests that were skipped or not executed. This provides a comprehensive inventory and helps diagnose missing or skipped tests.
-   **`ResultMixin`**: Extends `unittest.TestResult` to gather detailed information about the outcome of each test, including success, failure, errors, skips, and execution duration. It also uses `time.monotonic()` for precise duration tracking and provides full tracebacks for issues. This provides a rich dataset for analysis and reporting.

## Usage

### `TimingMixin` and `InventoryMixin`

To use `TimingMixin` or `InventoryMixin`, simply inherit from them in your `unittest.TestCase` classes:

```python
import unittest
from unittest_observability import TimingMixin, InventoryMixin

class MyTests(TimingMixin, InventoryMixin, unittest.TestCase):
    def test_example(self):
        # Your test code
        self.assertTrue(True)

# To access inventory:
# inventory = MyTests.get_test_inventory()
```

`TimingMixin` will automatically print timing statistics to `sys.stdout` after the test class finishes. `InventoryMixin` will print its report in `tearDownClass`.

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

This project uses GitHub Actions for continuous integration and publishing. A workflow is configured to build and publish the package to TestPyPI on pushes to the `main` branch or when a new tag (e.g., `v1.0.0`) is created. Ensure you have a `TEST_PYPI_API_TOKEN` GitHub Secret configured for publishing.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes.
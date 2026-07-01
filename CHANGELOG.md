# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2023-10-27

### Added

- GitHub Actions workflow for publishing to TestPyPI (`.github/workflows/publish.yml`).

### Fixed

- Resolved `ValueError` in `ResultMixin._add_result` when handling skipped tests.
- Corrected `test_result_mixin_collection` assertion for `InventoryMixin` to account for skipped tests not calling `setUp`.

### Changed

- Marked `test_failure_case` and `test_error_case` with `@unittest.expectedFailure` in `test_result_mixin.py`.
- Refactored `TimingMixin` to no longer inherit from `unittest.TestCase`, making it a pure mixin.
- Reorganized project structure:
    - `timing_mixin.py` and `inventory_mixin.py` moved to `src/unittest_observability/testcase/mixins/`.
    - `result_mixin.py` moved to `src/unittest_observability/testresult/`.
- Updated all internal and test import paths to reflect the new project structure.
- Updated `src/unittest_observability/__init__.py` to expose mixins at the top-level for simplified imports.
- Switched `TimingMixin` and `ResultMixin` to use `time.monotonic()` for more accurate duration measurements.
- **Enhanced `InventoryMixin`**: Now discovers all test methods in `setUpClass` and reports on discovered, ran, and skipped tests in `tearDownClass`.
- Updated `README.md` usage examples to reflect simplified top-level imports and new structure.

## [0.1.0] - 2023-10-27

### Added

- Initial project setup with `src/` and `tests/` directories.
- `pyproject.toml` for package metadata and build configuration.
- `.gitignore` and `LICENSE` (Apache-2.0).
- `TimingMixin` for measuring test execution time.
- `InventoryMixin` for collecting executed test identifiers.
- `ResultMixin` for detailed test outcome collection.
- Test cases for `TimingMixin`, `InventoryMixin`, and `ResultMixin`.
- `setup_dev_env.bat` for easy development environment setup.

### Changed

- Renamed `TestInventoryMixin` to `InventoryMixin`.
- Renamed `TestResultMixin` to `ResultMixin`.
- Updated `pyproject.toml` with author details, Python 3.12+ requirement, and Apache-2.0 license.
- Removed `main.py` and `test_main.py` as they are not part of the core library.
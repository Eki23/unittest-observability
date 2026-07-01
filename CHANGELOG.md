# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

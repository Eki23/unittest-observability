# Copyright (c) 2026 Christian Ekiza

import unittest
import time

class ResultMixin(unittest.TestResult):
    """
    A mixin for unittest.TestResult to collect detailed information about test outcomes.
    """
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        super().__init__(stream, descriptions, verbosity)
        self.test_results = []
        self._current_test_start_time = None

    def startTest(self, test):
        self._current_test_start_time = time.monotonic() # Changed to monotonic
        super().startTest(test)

    def _add_result(self, test, outcome, err=None, reason=None):
        end_time = time.monotonic() # Changed to monotonic
        duration = end_time - self._current_test_start_time if self._current_test_start_time else 0
        result_info = {
            "id": test.id(),
            "description": test.shortDescription(),
            "outcome": outcome,
            "duration": duration,
            "error": str(err[1]) if err and isinstance(err, tuple) else None,
            "traceback": self._exc_info_to_string(err, test) if err and isinstance(err, tuple) else None,
            "reason": reason,
        }
        self.test_results.append(result_info)
        self._current_test_start_time = None # Reset for the next test

    def addSuccess(self, test):
        self._add_result(test, "success")
        super().addSuccess(test)

    def addFailure(self, test, err):
        self._add_result(test, "failure", err)
        super().addFailure(test, err)

    def addError(self, test, err):
        self._add_result(test, "error", err)
        super().addError(test, err)

    def addSkip(self, test, reason):
        self._add_result(test, "skipped", err=None, reason=reason)
        super().addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        self._add_result(test, "expected_failure", err)
        super().addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        self._add_result(test, "unexpected_success")
        super().addUnexpectedSuccess(test)

    def get_collected_results(self):
        """
        Returns a list of dictionaries, each containing details about a test's execution.
        """
        return self.test_results
import time
import statistics

class TimingMixin: # Removed inheritance from unittest.TestCase
    """
    A mixin for unittest.TestCase to observe total test class timing
    and provide statistics about individual test method timings.
    """
    _class_start_time = None
    _method_timings = [] # Stores {'id': test_id, 'duration': duration} for methods in this class

    @classmethod
    def timing_class_setup(cls) -> str:
        """
        Proxy method to initialize timing for the class.
        Should be called within the subclass's setUpClass method.
        Returns a string indicating the action.
        """
        cls._class_start_time = time.monotonic()
        cls._method_timings = []
        return f"Timing for class {cls.__name__} initialized at {cls._class_start_time}."

    @classmethod
    def timing_class_teardown(cls) -> dict:
        """
        Proxy method to finalize timing for the class and return statistics.
        Should be called within the subclass's tearDownClass method.
        Returns a dictionary containing timing statistics.
        """
        class_end_time = time.monotonic()
        class_duration = class_end_time - cls._class_start_time if cls._class_start_time else 0

        stats = {
            "class_name": cls.__name__,
            "total_class_duration": class_duration,
            "method_timings": []
        }

        if cls._method_timings:
            durations = [t['duration'] for t in cls._method_timings]
            total_methods_duration = sum(durations)
            avg_duration = statistics.mean(durations)
            min_duration = min(durations)
            max_duration = max(durations)

            stats["total_methods_duration"] = total_methods_duration
            stats["num_test_methods"] = len(cls._method_timings)
            stats["average_method_duration"] = avg_duration
            stats["min_method_duration"] = min_duration
            stats["max_method_duration"] = max_duration
            stats["method_timings"] = sorted(cls._method_timings, key=lambda x: x['duration'], reverse=True)
        else:
            stats["message"] = "No test method timings collected."
        
        # Optionally, you can still print for immediate console feedback if desired
        print(f"\n--- Timing Statistics for Test Class: {cls.__name__} ---")
        print(f"Total Class Duration: {stats['total_class_duration']:.4f} seconds")
        if "num_test_methods" in stats:
            print(f"Total Method Execution Time: {stats['total_methods_duration']:.4f} seconds")
            print(f"Number of Test Methods: {stats['num_test_methods']}")
            print(f"Average Method Duration: {stats['average_method_duration']:.4f} seconds")
            print(f"Min Method Duration: {stats['min_method_duration']:.4f} seconds")
            print(f"Max Method Duration: {stats['max_method_duration']:.4f} seconds")
            print("Individual Method Durations (longest first):")
            for timing in stats['method_timings']:
                print(f"  - {timing['id']}: {timing['duration']:.4f} seconds")
        else:
            print(stats["message"])
        print("--------------------------------------------------")

        return stats

    def timing_method_setup(self) -> str:
        """
        Proxy method to initialize timing for an individual test method.
        Should be called within the subclass's setUp method.
        Returns a string indicating the action.
        """
        self._method_start_time = time.monotonic()
        return f"Timing for method {self.id()} initialized at {self._method_start_time}."

    def timing_method_teardown(self) -> dict:
        """
        Proxy method to finalize timing for an individual test method.
        Should be called within the subclass's tearDown method.
        Returns a dictionary with the method ID and its duration.
        """
        method_end_time = time.monotonic()
        method_duration = (
            method_end_time - self._method_start_time if hasattr(self, '_method_start_time') else 0
        )
        # self.id() is a method of unittest.TestCase, which the class mixing this will inherit from
        method_timing_data = {
            'id': self.id(),
            'duration': method_duration
        }
        self.__class__._method_timings.append(method_timing_data)
        return method_timing_data
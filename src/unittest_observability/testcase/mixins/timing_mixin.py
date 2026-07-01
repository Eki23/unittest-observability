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
    def setUpClass(cls):
        # Call super().setUpClass() first to ensure TestCase's setUpClass runs
        super().setUpClass() 
        cls._class_start_time = time.time()
        cls._method_timings = [] # Ensure it's fresh for each class

    @classmethod
    def tearDownClass(cls):
        # Call super().tearDownClass() first to ensure TestCase's tearDownClass runs
        super().tearDownClass()
        class_end_time = time.time()
        class_duration = class_end_time - cls._class_start_time if cls._class_start_time else 0

        print(f"\n--- Timing Statistics for Test Class: {cls.__name__} ---")
        print(f"Total Class Duration: {class_duration:.4f} seconds")

        if cls._method_timings:
            durations = [t['duration'] for t in cls._method_timings]
            total_methods_duration = sum(durations)
            avg_duration = statistics.mean(durations)
            min_duration = min(durations)
            max_duration = max(durations)

            print(f"Total Method Execution Time: {total_methods_duration:.4f} seconds")
            print(f"Number of Test Methods: {len(cls._method_timings)}")
            print(f"Average Method Duration: {avg_duration:.4f} seconds")
            print(f"Min Method Duration: {min_duration:.4f} seconds")
            print(f"Max Method Duration: {max_duration:.4f} seconds")
            print("Individual Method Durations (longest first):")
            for timing in sorted(cls._method_timings, key=lambda x: x['duration'], reverse=True):
                print(f"  - {timing['id']}: {timing['duration']:.4f} seconds")
        else:
            print("No test method timings collected.")
        print("--------------------------------------------------")

    def setUp(self):
        # Call super().setUp() first to ensure TestCase's setUp runs
        super().setUp()
        self._method_start_time = time.time()

    def tearDown(self):
        # Call super().tearDown() first to ensure TestCase's tearDown runs
        super().tearDown()
        method_end_time = time.time()
        method_duration = method_end_time - self._method_start_time
        # self.id() is a method of unittest.TestCase, which the class mixing this will inherit from
        self.__class__._method_timings.append({
            'id': self.id(), 
            'duration': method_duration
        })
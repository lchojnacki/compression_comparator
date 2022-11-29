import timeit
from contextlib import AbstractContextManager


class MeasureExecutionTime(AbstractContextManager):
    def __init__(self, name: str | None = None):
        self.name = name or ""
        self.execution_time = 0

    def __enter__(self):
        self.start = timeit.default_timer()
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.execution_time = (timeit.default_timer() - self.start) * 1000.0

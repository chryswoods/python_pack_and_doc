
import cython


__all__ = ["FastClass", "fast_function"]


class FastClass:
    """A class with some functions that are compiled"""
    def __init__(self):
        pass

    def func(self):
        cdef int i = 0
        cdef float x = 0.0
        cdef float y = 0.0

        for i in range(0, 10):
            x = 5.0 * i
            y = x * x

        print(f"y = {y}")


def fast_function():
    """A function that is compiled"""
    cdef int i = 0
    cdef float x = 0.0
    cdef float y = 0.0

    for i in range(0, 10):
        x = 5.0 * i
        y = x * x

    print(f"y = {y}")

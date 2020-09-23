
__all__ = ["ExampleClass"]


class ExampleClass:
    """This is an example class. Place it's documentation here."""

    def __init__(self):
        """Documentation for the constructor"""
        print("Constructing an ExampleClass")

    def func(self):
        """This is an example function"""
        print("Calling ExampleClass.func()")

    def _hidden_func(self):
        """This is a hidden function"""
        print("Calling ExampleClass._hidden_func()")

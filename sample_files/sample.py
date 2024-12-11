import os
import sys

class CompliantClass:
    """This is a sample class with a compliant name."""

    def compliant_method(self, param: int) -> int:
        """A method with proper naming and type annotations."""
        return param * 2

    def non_compliantMethod(self):
        pass


class Noncompliantclass:
    """This class has a non-compliant name."""

    def compliant_method(self, param: str) -> str:
        """A properly named method with type annotations."""
        return param.upper()


def compliant_function(param: float) -> float:
    """A top-level function with proper naming and annotations."""
    return param * 2.5


def nonCompliantFunction():
    pass

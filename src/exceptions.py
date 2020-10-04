"""
Here is stored all exceptions.
"""


class MainException(Exception):
    """
    Base exceptions of all exceptions of this package.
    """


class UnrecognizedArgument(MainException):
    """
    When an argument is invalid.
    """


class MissRequired(MainException):
    """
    When something required is missing.
    """


class InvalidCombination(MainException):
    """
    When a combination of something is invalid.
    """


class BadReference(MainException):
    """
    When referring to something that is not expected.
    """


class InvalidConfiguration(MainException):
    """
    When a configuration is invalid.
    """


class WrongFileFormat(MainException):
    """
    When a file is in an unexpected format.
    """

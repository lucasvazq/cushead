"""
Exceptions declaration.
"""


class MainException(Exception):
    """
    Base exception for all exceptions of this package.
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


class InvalidConfig(MainException):
    """
    When a config is invalid.
    """


class WrongFileFormat(MainException):
    """
    When a file is in an unexpected format.
    """

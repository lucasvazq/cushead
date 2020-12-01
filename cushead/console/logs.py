"""
Execute custom print messages.
"""
import argparse
import pathlib
import textwrap
from typing import List

import colorama

from cushead import info
from cushead.console.arguments import files_creator


def show_presentation() -> None:
    """
    Print the presentation message.
    """
    presentation_message = textwrap.dedent(
        f"""\
          ____  _   _  ____   _   _  _____     _     ____     ____ __   __
         / ___|| | | |/ ___| | | | || ____|   / \\   |  _ \\   |  _ \\\\ \\ / /
        | |    | | | |\\___ \\ | |_| ||  _|    / _ \\  | | | |  | |_) |\\ V /
        | |___ | |_| | ___) ||  _  || |___  / ___ \\ | |_| |_ |  __/  | |
         \\____| \\___/ |____/ |_| |_||_____|/_/   \\_\\|____/(_)|_|     |_|
                                     __       _
                                     _/     /
                                    /    __/
                UX / SEO          _/  __/           v {info.PACKAGE_VERSION}
                                 / __/
                                / /
                               /'

        Author: {info.AUTHOR}
        Email: {info.EMAIL}
        Page: {info.AUTHOR_PAGE}
        License: {info.PACKAGE_LICENSE}

        Source: {info.SOURCE}
        Documentation: {info.DOCUMENTATION}
        For help run: {info.PACKAGE_NAME} -h
        """
    )
    print(f"{colorama.Fore.BLUE}{presentation_message}{colorama.Fore.RESET}")


def get_exception_message(*, parser: argparse.ArgumentParser, message: str) -> str:
    """
    Generate exception message with argparse format.

    Args:
        parser: a parser instance.
        message: the message.

    Returns:
        The message.
    """
    return "\n".join(
        (
            f"usage: {parser.usage}",
            f"{info.PACKAGE_NAME}: error: {message}",
        ),
    )


def show_created_file(path: pathlib.Path) -> None:
    """
    Print a created file message.
    """
    print(f" - {path.parent}/{colorama.Fore.YELLOW}{path.name}{colorama.Fore.RESET}")


def show_created_file_errors(errors: List[files_creator.Error]) -> None:
    """
    Print error messages for the files with errors at creation time.
    """
    if not errors:
        return

    print("\nErrors:")
    for error in errors:
        print(f" - {colorama.Fore.RED}{error.error}{colorama.Fore.RESET}: {error.path.parent}/{colorama.Fore.YELLOW}{error.path.name}{colorama.Fore.RESET}")

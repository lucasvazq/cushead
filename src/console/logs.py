"""
Module used to store things related to the console presentation.
"""
import textwrap

import colorama

from src import info


def show_presentation() -> None:
    """
    Print the console presentation message.
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

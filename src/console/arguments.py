import argparse
import textwrap

from src import helpers
from src import info
from src.base import logs


def setup_parser() -> argparse.ArgumentParser:
    """doc"""
    package_info = info.get_info()
    name = package_info.package_name
    parser = argparse.ArgumentParser(
        prog=package_info.package_name,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=f"{package_info.package_name} -config FILEPATH",
        epilog=textwrap.dedent(f"""\
            Examples:
            1) Generate default config file with images:
                {name} -default settings.json --images
            2) Run that config:
                {name} -config settings.json
        """),
    )

    main_arguments = parser.add_argument_group("Main arguments")
    complementary_arguments = parser.add_argument_group("Complementary")

    # GROUP: required
    # -config
    main_arguments.add_argument(
        "-config",
        metavar="FILEPATH",
        dest="config",
        help="Path to a config file in JSON format. Read a config file and create the main files based on it.",
    )
    # -default
    main_arguments.add_argument(
        "-default",
        metavar="FILENAME",
        dest="default",
        help="Path to output a default config file. Can use with --images",
    )
    # GROUP: options
    # -images
    images_names_list = (image.name for image in helpers.get_images_list())
    joined_words = helpers.string_list_union(string_list=images_names_list)
    complementary_arguments.add_argument(
        "--images",
        dest="images",
        action="store_true",
        help=(
            "Use with -default. Generate default images that can be used by the settings. "
            f"This include: {joined_words}"
        ),
    )

    parser.set_defaults(images=False)

    return parser


def validate_args(
    *,
    parser: argparse.ArgumentParser,
    args: list,
) -> argparse.ArgumentParser:
    """
    doc
    """

    unrecognized_args = parser.parse_known_args(args)[1]
    if unrecognized_args:
        logs.error_log(message=f"Unrecognized argument {unrecognized_args[0]}")

    # Re-parse arguments.
    parsed_args = parser.parse_args(args)

    if not (parsed_args.config or parsed_args.default):
        logs.error_log(message="Miss Required arguments. Use -config or -default. Use -h for help")
    if parsed_args.config and parsed_args.default:
        logs.error_log(message="Can't use -config and -default arguments together.")
    if parsed_args.images and not parsed_args.default:
        logs.error_log(message="Can't use --images without -default.")
    if parsed_args.config:
        error = helpers.path_is_not_directory(
            key="-config",
            file_path=parsed_args.config,
        )
        if error:
            logs.error_log(message=error)

    return parsed_args


def parse_args(
    *,
    args: list
) -> argparse.Namespace:
    """
    doc
    """
    parser = setup_parser()
    parsed_args = validate_args(
        parser=parser,
        args=args,
    )
    return parsed_args

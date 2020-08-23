import argparse

from . import cli

# TODO: Auto/gen cli
# TODO: MultiRow & MultiColumn
# TODO: MultiRow RE
# TODO: Code Refactor
# TODO: README # EXAMPLES
# TODO: Protection whitespaces & CLI options
# TODO: Fix: Overlap Bug: (row,10 - 20, green) and (row, 10 - 30, left-green)
# TODO: Fix: Comments layout bug
# TODO: [OPTIONAL] Cli options & Size font (Size levels ...)


def main():
    parser = argparse.ArgumentParser(description="Locom is tool for generation commented log. "
                                                 "The output format is HTML. "
                                                 "For more information visit https://pypi.org/project/locom/.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers()

    cli_parser = subparsers.add_parser('cli')
    cli_parser.set_defaults(func=cli.run)

    cli_parser.add_argument("-r", "--rules-file",
                            required=True,
                            help="Rules describes recognition and rendering of rows.")
    cli_parser.add_argument("-i", "--input-file",
                            required=True,
                            help="Input log")
    cli_parser.add_argument("-o", "--output-file",
                            default="",
                            help="If output file is empty filename will be same as input file. "
                                 "Only suffix will be .html.")
    cli_parser.add_argument("-t", "--template",
                            default="dark",
                            help="The template for output html.")
    cli_parser.add_argument("--title",
                            default="",
                            help="The title for html output page.")
    cli_parser.add_argument("--description",
                            default="",
                            help="The description for html output page.")
    cli_parser.add_argument("--description-file",
                            default="",
                            help="HTML file with description for html output page.")
    cli_parser.add_argument("--row-number-column",
                            default="3",
                            help="The percentage size of row column in output html.")
    cli_parser.add_argument("--log-column",
                            default="64",
                            help="The percentage size of log column in output html.")
    cli_parser.add_argument("--mr-column",
                            default="2",
                            help="The percentage size of multi-row comment columns in output html.")
    cli_parser.add_argument("--cancel-whitespace-protection",
                            default="",
                            help="")
    cli_parser.add_argument("--cancel-escape-sequence-protection",
                            default="",
                            help="")

    generator_parser = subparsers.add_parser('gen')
    generator_parser.set_defaults(func=cli.generator)

    generator_parser.add_argument('--suffixes', type=str, nargs='+', default=["*.txt", "*.log"])

    auto_parser = subparsers.add_parser('auto')
    auto_parser.set_defaults(func=cli.auto)

    auto_parser.add_argument('--suffixes', type=str, nargs='+', default=["*.txt", "*.log"])

    arguments = parser.parse_args()
    arguments.func(arguments)


if __name__ == "__main__":
    main()

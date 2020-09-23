
def parse_args():
    """Parse all of the command line arguments"""
    import configargparse
    import sys

    configargparse.init_argument_parser(
        name="main",
        description="pack_and_doc example program",
        prog="pack_and_doc")

    parser = configargparse.get_argument_parser("main")

    parser.add_argument("--example", action="store_true",
                        default=None,
                        help="An example command line argument.")

    args = parser.parse_args()

    return (args, parser)


def cli():
    args, parser = parse_args()

    if args.example:
        print("You used --example")

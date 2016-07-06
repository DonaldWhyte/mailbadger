#!/usr/bin/python

"""Python script installed with setup.py to run mailbadger script."""

from moduledependency.main import get_argument_parser
from moduledependency.main import main

if __name__ == '__main__':
    parser = get_argument_parser()
    args = parser.parse_args()
    main(args)

#!/usr/bin/env python3

"""Python script installed with setup.py to run mailbadger script."""

from mailbadger.main import get_argument_parser
from mailbadger.main import main

if __name__ == '__main__':
    parser = get_argument_parser()
    args = parser.parse_args()
    main(args)

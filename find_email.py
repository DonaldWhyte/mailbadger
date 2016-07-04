#!/usr/bin/python

from email_finder.address_validator import AddressValidator
from email_finder.address_guesser import get_possible_addresses_for
import argparse

def get_argument_parser():
    parser = argparse.ArgumentParser(
        description='Search email server for possible emails belonging to specified individual')
    parser.add_argument('first_name', type=str, help='first name of person')
    parser.add_argument('second_name', type=str, help='second name of person')
    parser.add_argument('domain', type=str, help='domain of email server to search')
    parser.add_argument('--verbose', action='store_true', help="enable verbose output")
    parser.add_argument('--maxNumberToTry', type=int, default=10,
                        help='max number to append to candidate email')
    parser.add_argument('--numProcesses', type=int, default=10,
                        help='number of processes to spawn for validating emails in parallel')

    return parser

def main(args):
    # Generate set of possible email addresses the specified person may have
    candidate_addresses = get_possible_addresses_for(args.first_name,
                                                     args.second_name,
                                                     args.maxNumberToTry)
    # Validate candidate emails by checking if they exist on target email server
    validator = AddressValidator(args.numProcesses)
    addresses = validator.validate_addresses(candidate_addresses,
                                             args.domain,
                                             args.verbose)
    # Output found addresses
    for addr in addresses:
        print addr

if __name__ == '__main__':
    parser = get_argument_parser()
    args = parser.parse_args()
    main(args)

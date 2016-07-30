from mailbadger.address_validator import AddressValidator
from mailbadger.validator import Validator

import unittest
from unittest.mock import Mock

TEST_ADDRESSES = {
     # Address   # isValid
    'foo':       True,
    'donald':    True,
    '248592':    False,
    'contact':   True,
    'stuff':     False
}
TEST_DOMAIN = 'mailbadger.com'

# The underlying `AddressValidator` will pass mocks to other processed, which is
# not support by `Mock` by default. We manually implement a mock `validate`
# method that uases the preset test data and create a piackable mock class for
# `validate_mail_server`.
class PickableMock(Mock):
    def __reduce__(self):
        return (Mock, ())

def mock_validate(address, domain):
    if domain != TEST_DOMAIN:
        raise ValueError('domain passed in does not match expected domain: {}'.format(TEST_DOMAIN))
    return TEST_ADDRESSES[address]

def create_mock_underlying_validator(mailServiceIsValid):
    validator = Validator()
    validator.validate = mock_validate
    validator.validate_mail_server = PickableMock(return_value=mailServiceIsValid)
    return validator

class TestAddressValidator(unittest.TestCase):

    def setUp(self):
        underlying_validator = Mock()
        self._validator = AddressValidator(underlying_validator, 4)

    def test_validator_with_zero_processes(self):
        with self.assertRaisesRegex(ValueError, 'processes must be at least 1'):
            AddressValidator(Mock(), 0)

    def test_validator_with_one_process(self):
        underlying_validator = create_mock_underlying_validator(
            mailServiceIsValid=True)

        validator = AddressValidator(underlying_validator, 1)
        result = validator.validate_addresses(TEST_ADDRESSES.keys(), TEST_DOMAIN)

        self.assertCountEqual(
            ['foo@mailbadger.com', 'donald@mailbadger.com', 'contact@mailbadger.com' ],
            result)

    def test_validator_with_multiple_processes(self):
        underlying_validator = create_mock_underlying_validator(
            mailServiceIsValid=True)

        validator = AddressValidator(underlying_validator, 2)
        result = validator.validate_addresses(TEST_ADDRESSES.keys(), TEST_DOMAIN)

        self.assertCountEqual(
            ['foo@mailbadger.com', 'donald@mailbadger.com', 'contact@mailbadger.com' ],
            result)

    def test_validator_with_invalid_domain_server(self):
        underlying_validator = create_mock_underlying_validator(
            mailServiceIsValid=False)

        validator = AddressValidator(underlying_validator, 1)
        result = validator.validate_addresses(TEST_ADDRESSES.keys(), TEST_DOMAIN)

        self.assertCountEqual([], result)

    def test_validator_with_no_addresses_passed(self):
        underlying_validator = create_mock_underlying_validator(
            mailServiceIsValid=True)

        validator = AddressValidator(underlying_validator, 1)
        result = validator.validate_addresses([], TEST_DOMAIN)

        self.assertCountEqual([], result)

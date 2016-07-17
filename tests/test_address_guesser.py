from mailbadger.address_guesser import get_possible_addresses_for

import unittest

class TestAddressGuesser(unittest.TestCase):

    def test_empty_first_name(self):
        self.assertEqual(get_possible_addresses_for('', 'Whyte'), { 'Whyte' })

    def test_empty_last_name(self):
        self.assertEqual(get_possible_addresses_for('Donald', ''), { 'Donald' })

    def test_first_and_last_name(self):
        self.assertEqual(get_possible_addresses_for('Donald', 'Whyte'), {
            'DWhyte', 'D.Whyte', 'Donald.W', 'Whyte',
            'DonaldW', 'Donald', 'DonaldWhyte', 'Donald.Whyte'
        })

    def test_max_num_to_try_is_zero(self):
        self.assertEqual(get_possible_addresses_for('Donald', '', 0), {
            'Donald', 'Donald0'
        })

        self.assertEqual(get_possible_addresses_for('', 'Whyte', 0), {
            'Whyte', 'Whyte0'
        })

        self.assertEqual(get_possible_addresses_for('Donald', 'Whyte', 0), {
            'DWhyte', 'D.Whyte', 'Donald.W', 'Whyte',
            'DonaldW', 'Donald', 'DonaldWhyte', 'Donald.Whyte',
            'DWhyte0', 'D.Whyte0', 'Donald.W0', 'Whyte0',
            'DonaldW0', 'Donald0', 'DonaldWhyte0', 'Donald.Whyte0',
        })

    def test_max_num_to_try_is_one(self):
        self.assertEqual(get_possible_addresses_for('Donald', '', 1), {
            'Donald', 'Donald0', 'Donald1'
        })

        self.assertEqual(get_possible_addresses_for('', 'Whyte', 1), {
            'Whyte', 'Whyte0', 'Whyte1'
        })

        self.assertEqual(get_possible_addresses_for('Donald', 'Whyte', 1), {
            'DWhyte', 'D.Whyte', 'Donald.W', 'Whyte',
            'DonaldW', 'Donald', 'DonaldWhyte', 'Donald.Whyte',
            'DWhyte0', 'D.Whyte0', 'Donald.W0', 'Whyte0',
            'DonaldW0', 'Donald0', 'DonaldWhyte0', 'Donald.Whyte0',
            'DWhyte1', 'D.Whyte1', 'Donald.W1', 'Whyte1',
            'DonaldW1', 'Donald1', 'DonaldWhyte1', 'Donald.Whyte1',
        })

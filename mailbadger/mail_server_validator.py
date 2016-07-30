from mailbadger.validator import Validator
from validate_email import validate_email
import logging

SERVER_TEST_ADDRESS = 'test@{domain}'

OBVIOUSLY_FAKE_ADDRESSES = [
    'poo.thisisfake'
    'agh12345djfj',
    'zvngh99fla',
    'bogardcaof',
    '975489qyewof9y__esr78ye4847t____',
    '1234567wgjskxSNFJBGvje5___________SSSAJWNN',
    'foofoofoofoofoofoofooBLAHBLAHBLAHhahahah2742'
]

class MailServerValidator(Validator):

    def validate(self, address, domain):
        try:
            full_address = '{addr}@{domain}'.format(addr=address, domain=domain)
            result = validate_email(full_address, verify=True)

            if result:
                logging.info('{email} exists'.format(email=address))
            else:
                logging.info('{email} does not exist'.format(email=address))

            return result
        except TimeoutError as e:
            logging.info('Timed out validating {email}'.format(email=address))
            return False

    def validate_mail_server(self, domain):
        can_talk_to = validate_email(SERVER_TEST_ADDRESS.format(domain=domain),
                                     check_mx=True)

        if not can_talk_to:
            msg = 'Cannot detect mail server at "{domain}"'
            logging.error(msg.format(domain=domain))
            return False

        # Some mail servers always say every email you request exists. To
        # prevent those servers misleading users, we consider the mail server
        # invalid if they say every email address from a collection of obviously
        # fake addresses exist.
        fakeEmails = [
            '{:s}@{:s}'.format(addr, domain) for addr in OBVIOUSLY_FAKE_ADDRESSES
        ]
        fakeEmailExistences = [
            self.validate(email, domain) for email in fakeEmails
        ]
        if all(exists == True for exists in fakeEmailExistences):
            msg = 'Mail server at {domain} said all fake dummy addresses'
            msg += ' exist, cannot use it for validating addresses'
            logging.error(msg.format(domain=domain))
            return False

        return True

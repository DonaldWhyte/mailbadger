from validate_email import validate_email
from DNS.Base import TimeoutError
from multiprocessing import Pool
import logging
from functools import partial

def validate(addr, verbose=False):
    try:
        result = validate_email(addr, verify=True)

        if verbose:
            if result:
                print '{email} exists'.format(email=addr)
            else:
                print '{email} does not exist'.format(email=addr)

        if not result:
            result = False
        return (addr, result)
    except TimeoutError as e:
        msg = 'Timed out validating {email}'.format(email=addr)
        if verbose:
            print msg
        logging.info(msg)

        return (addr, False)

class AddressValidator:

    def __init__(self, numProcesses):
        self.proc_pool = Pool(numProcesses)

    def validate_addresses(self, addresses, domain, verbose=False):
        # ensure domain has a detectable SMTP server before doing anything
        if not validate_email('test@{domain}'.format(domain=domain), check_mx=True):
            msg = 'Cannot detect mail server at "{domain}"'.format(domain=domain)
            if verbose:
                print msg
            logging.info(msg)
            return []

        # validate the specified addresses exist on the specified domain
        addresses = [ '{:s}@{:s}'.format(addr, domain) for addr in addresses ]
        validateFunc = partial(validate, verbose=verbose)
        results = self.proc_pool.map(validateFunc, addresses)

        # only return addresses which exist
        return [ res[0] for res in results if res[1] ]

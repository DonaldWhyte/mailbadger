from validate_email import validate_email
from DNS.Base import TimeoutError
from multiprocessing import Pool
import logging
from functools import partial
import signal

TIMEOUT = 999999999

def _validate(addr, verbose=False):
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

    def __init__(self, num_processes):
        self._num_processes = num_processes
        self._create_pool()

    def _create_pool(self):
        # Make the process ignore SIGINT before a process Pool is created. This
        # way created child processes inherit SIGINT handler.
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.proc_pool = Pool(self._num_processes)
        # Restore the original SIGINT handler in the parent process after a Pool
        # has been created.
        signal.signal(signal.SIGINT, original_sigint_handler)

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
        validate_func = partial(_validate, verbose=verbose)

        # Use `map_async()` so we can gracefully handle keyboard interrupts.
        # We want the interrupt to terminal *all* child processes, which won't
        # happen with the blocking `map()` call.
        pool_is_terminated = False
        interrupt_to_raise = None
        try:
            async_results = self.proc_pool.map_async(validate_func, addresses)
            results = async_results.get(TIMEOUT) # need timeout for interrupt to work
        except KeyboardInterrupt as e:
            self.proc_pool.terminate()
            interrupt_to_raise = e
        self.proc_pool.join()

        # Recreate the process pool if it was terminated by keyboard interrupt,\
        # then continue bubbling the interrupt upwards. Yes, this is hacky.
        # Yes, I feel dirty. But gracefully handling keyboard interrupts is
        # important
        if interrupt_to_raise:
            self._create_pool()
            raise e

        # only return addresses which exist
        return [ res[0] for res in results if res[1] ]

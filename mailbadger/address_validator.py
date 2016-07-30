from DNS.Base import TimeoutError
from multiprocessing import Pool
from itertools import repeat
import signal
import logging

TIMEOUT = 999999999

def validate_wrapper((validator, address, domain)):
    return (address, validator.validate(address, domain))

class AddressValidator:

    def __init__(self, validator, num_processes):
        self._validator = validator
        self._num_processes = num_processes

    def _create_pool(self):
        # Make the process ignore SIGINT before a process Pool is created. This
        # way created child processes inherit SIGINT handler.
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        proc_pool = Pool(self._num_processes)
        # Restore the original SIGINT handler in the parent process after a Pool
        # has been created.
        signal.signal(signal.SIGINT, original_sigint_handler)

        return proc_pool

    def validate_addresses(self, addresses, domain):
        if not self._validator.validate_mail_server(domain):
            return []

        # Use `map_async()` so we can gracefully handle keyboard interrupts.
        # We want the interrupt to terminal *all* child processes, which won't
        # happen with the blocking `map()` call.
        #
        # TODO: handle interrupts gracefully *and* don't recreate pool in every
        # call.
        pool = self._create_pool()
        interrupt_to_raise = None
        try:
            map_args = zip(repeat(self._validator), addresses, repeat(domain))
            async_results = pool.map_async(validate_wrapper, map_args)
            results = async_results.get(TIMEOUT) # need timeout for interrupt to work
        except KeyboardInterrupt as e:
            pool.terminate()
            interrupt_to_raise = e
        else:
            pool.close()
        pool.join()

        if interrupt_to_raise:   # bubble interrupt up the call stack
            raise e

        # only return addresses which exist
        return [ res[0] for res in results if res[1] ]

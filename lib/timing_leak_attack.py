
import time
import subprocess
import os
import mechanize
import copy

import lib.utils as utils

# Length of the signature in hex string.
SIGNATURE_LEN = 40

class SignatureFound(Exception):
    '''When the correct signature is found, the program raises this exception to signal it and exit the search.'''
    pass


def config_browser():
    '''Returns Browers instance fully configured.'''
    browser = mechanize.Browser()
    browser.set_handle_equiv(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent', 'Firefox')]
    return browser

def try_signature(browser, signature):
    '''Returns the total time it took to check the signature or None if signature was correct.'''
    start_time = time.time()
    try:
        browser.open("http://localhost:8080/test?file=foo&signature={}".format(signature))
    except:
        elapsed_time = time.time() - start_time
        return elapsed_time

def rjust_signature(signature):
    return signature.ljust(SIGNATURE_LEN, '0')

@utils.static_var('comms_latency', None)
def is_previous_guess_wrong(timeouts, signature, server_timeout):
    '''Checks whether we should revert back to the previous guess because no new byte causes delay to be bigger.'''

    # We get all but the greatest 5 times.
    all_times = copy.copy(timeouts.values())
    sorted(all_times)
    all_times_filtered = all_times[:-5]
    avg_time = sum(all_times_filtered) / len(all_times_filtered)

    # If we are guessing the first byte, we have to calculate the communitations latency.
    if not signature and not is_previous_guess_wrong.comms_latency:
        is_previous_guess_wrong.comms_latency = avg_time - server_timeout
        print 'setting comms_latency to', is_previous_guess_wrong.comms_latency

    # this is the minimum time every comparison should take, otherwise we have previously guessed some incorrect bytes.
    minimum_timeout = (len(signature) + 1) * server_timeout + is_previous_guess_wrong.comms_latency

    if avg_time < minimum_timeout:
        print 'avg_time greater than server_timeout'
        return True
    else:
        return False

def get_next_byte_timeouts(browser, signature):
    timeouts = {}
    for value in xrange(0,256):
        candidate = hex(value)[2:].rjust(2, '0')
        candidate_signature = rjust_signature(''.join(signature) + candidate)
        timeout = try_signature(browser, candidate_signature)
        if not timeout:
            print len(signature), SIGNATURE_LEN, len(signature) == (SIGNATURE_LEN / 2 - 1)
            signature.append(candidate)
            raise SignatureFound()
        timeouts[candidate] = try_signature(browser, candidate_signature)
    return timeouts

def get_best_candidate(timeouts):
    return max(timeouts.items(), key=lambda x: x[1])

def find_signature(browser, server_timeout):
    '''Returns signature in hex string.'''
    signature = []
    try:
        # Iterate until the signature is found or an error occur.
        while True:
            # First, we get the processing times for all possible options.
            timeouts = get_next_byte_timeouts(browser, signature)

            # Now we check whether something has gone wrong and our previous guess is wrong.
            if is_previous_guess_wrong(timeouts, signature, server_timeout):
                signature = signature[:-1]
            else:
                signature.append(get_best_candidate(timeouts)[0])
                print "signature is", signature

    except SignatureFound:
        print "Signature has been found:", signature
        return ''.join(signature)

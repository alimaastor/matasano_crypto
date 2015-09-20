
import os
import subprocess
import atexit

import lib.utils as utils
from lib.timing_leak_attack import find_signature, config_browser

p = None

def close_server():
    try:
        p.terminate()
    except:
        pass

def main():
    # Init variables.
    os.environ['SERVER_TIMEOUT'] = "0.050"
    server_timeout = float(os.environ['SERVER_TIMEOUT'])
    print 'comparison time for each byte is', server_timeout, 'seconds'

    # Start server.
    command = 'python {}'.format(os.path.join('lib', 'timing_leak_server.py'))
    with open(os.devnull, 'rw') as devnull:
        global p
        p = subprocess.Popen(command, shell=True, stdout=devnull, stderr=devnull)
    print 'server started'
    atexit.register(close_server)

    # Create browser and configure.
    browser = config_browser()

    # Find signature.
    signature = find_signature(browser, server_timeout)

    print 'signature is', signature

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description=('Implement and break HMAC-SHA1 with an artificial '
                     'timing leak - Challenge 31 (Set 4) of Matasano Crypto Challenge.'))

    args = parser.parse_args()

    try:
        main()
    except KeyboardInterrupt:
        pass


import os
import subprocess

import lib.utils as utils
from lib.timing_leak_attack import find_signature, config_browser

def main():
    # Init variables.
    os.environ['SERVER_TIMEOUT'] = "0.005"
    server_timeout = float(os.environ['SERVER_TIMEOUT'])
    print 'comparison time for each byte is', server_timeout, 'seconds'

    # Start server.
    command = 'python {}'.format(os.path.join('lib', 'timing_leak_server.py'))
    with open(os.devnull, 'rw') as devnull:
        p = subprocess.Popen(command, shell=True, stdout=devnull, stderr=devnull)
    print 'server started'

    # Create browser and configure.
    browser = config_browser()

    # Find signature.
    signature = find_signature(browser, server_timeout)

    print 'signature is', signature

    p.terminate()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description=('Break HMAC-SHA1 with a slightly less artificial timing leak'
                     ' - Challenge 32 (Set 4) of Matasano Crypto Challenge.'))

    args = parser.parse_args()

    try:
        main()
    except KeyboardInterrupt:
        pass


import os
import subprocess
import sys
try:
    import web
except ImportError:
    print 'You have to install wep.py in order to run this script'
    sys.exit(1)


import lib.utils as utils
from lib.timing_leak_attack import find_signature, config_browser

def main(args):
    # Init variables.
    os.environ['SERVER_TIMEOUT'] = "0.005"
    server_timeout = float(os.environ['SERVER_TIMEOUT'])
    print 'comparison time for each byte is', server_timeout, 'seconds'

    if not args.no_server:
        # Start server.
        command = 'python {}'.format(os.path.join('lib', 'timing_leak_server.py'))
        p = subprocess.Popen(command, shell=True)
        print 'server started'

    # Create browser and configure.
    browser = config_browser()

    # Find signature.
    signature = find_signature(browser, server_timeout)

    print 'signature is', signature

    # Stop server.
    if not args.no_server:
        p.terminate()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description=('Break HMAC-SHA1 with a slightly less artificial timing leak'
                     ' - Challenge 32 (Set 4) of Matasano Crypto Challenge.'))
    parser.add_argument('--no-server',
        help='Don\'t run the timing leak server.', action='store_true')
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        pass

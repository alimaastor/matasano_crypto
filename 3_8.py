
import argparse
import time
import random

from lib.Message import Message
from lib.MerseneTwister import MerseneTwister, MerseneTwisterCypher, get_state_from_number

def main():
    mtc = MerseneTwisterCypher('password')

    # First we have to encrypt a known text for the whole state.
    print 'Generating encrypted text ...'
    plaintext = 'a' * MerseneTwister.N_CHARS_PER_STATE * MerseneTwister.STATE_LENGTH
    encrypted_message = mtc.encrypt(plaintext)

    # Now we get the state.
    print 'Calculating Mersene Twister state ...'
    whole_state = map(
            lambda output: int(str(get_state_from_number(Message(output).to_int()))),
            Message(encrypted_message).xor_whole(plaintext).slices(MerseneTwister.N_CHARS_PER_STATE),
        )

    # We clone the PRNG and we use it to create our own cypher.
    print 'Cloning cypher ...'
    mt_clone = MerseneTwister()
    mt_clone.set_state_and_index(whole_state, 0)
    mtc_clone = MerseneTwisterCypher()
    mtc_clone.mt = mt_clone

    # And finally we test it.
    print 'Testing result ...'
    assert mtc_clone.encrypt(mtc.encrypt(plaintext)) == plaintext, 'something went wrong'

    print 'Done'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create the MT19937 stream cipher and break it - Challenge 24 (Set 3) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

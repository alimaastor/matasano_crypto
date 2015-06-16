
import argparse
import time
import random

from lib.Message import Message
from lib.MerseneTwister import MerseneTwister, MerseneTwisterCypher, get_state_from_number

def main():
    mtc = MerseneTwisterCypher('a')
    # First we have to encrypt a known text for the whole state.
    plaintext = 'a' * MerseneTwister.N_CHARS_PER_STATE * MerseneTwister.STATE_LENGTH
    encrypted_message = mtc.encrypt(plaintext)

    # outputs = map(
    #     lambda x: Message(x).to_int(),
    #     Message(encrypted_message)
    #         .xor(plaintext)
    #         .slices(MerseneTwister.N_CHARS_PER_STATE)
    # )

    for i, (a, b) in enumerate(zip(Message(encrypted_message).slices(MerseneTwister.N_CHARS_PER_STATE), mtc.p)):
        if Message(a).xor(Message().set_int(b).to_str()).to_str() != 'aaaa':
            print "BBB for i {}; {} != {}".format(i, a, b)

    for i, (a, b) in enumerate(zip(outputs, mtc.p)):
        if a != b:
            print "AAA for i {}; {} != {}".format(i, a, b)

    raw_input()

    # Now we get the state.
    whole_state = map(
            lambda output: int(str(get_state_from_number(Message(output).to_int()))),
            Message(encrypted_message).xor(plaintext).slices(MerseneTwister.N_CHARS_PER_STATE),
        )

    for i, (a, b) in enumerate(zip(whole_state, mtc.mt.state)):
        if a != b:
            print "for i {}; {} != {}".format(i, a, b)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create the MT19937 stream cipher and break it - Challenge 24 (Set 3) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

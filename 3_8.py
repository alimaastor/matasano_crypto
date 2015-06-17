
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


    for i, (a, b) in enumerate(zip(Message(encrypted_message).slices(MerseneTwister.N_CHARS_PER_STATE), mtc.p)):
        if Message(a).xor_whole(Message().set_int(b).to_str()).to_str() != 'aaaa':
            print "BBB for i {}; {} != {}".format(i, a, b)

    # outputs = map(
    #     lambda x: Message(x).to_int(),
    #     Message(encrypted_message)
    #         .xor_whole(plaintext)
    #         .slices(MerseneTwister.N_CHARS_PER_STATE)
    # )

    a = [c for c in Message(encrypted_message).slices(MerseneTwister.N_CHARS_PER_STATE)]
    b = [c for c in Message(plaintext).slices(MerseneTwister.N_CHARS_PER_STATE)]
    assert len(a) == len(b)
    assert len(encrypted_message) == len(plaintext)

    outputs = []
    for i, ((encrypted_msg, plaintext_msg), c) in enumerate( \
                        zip(zip( \
                            Message(encrypted_message).slices(MerseneTwister.N_CHARS_PER_STATE), \
                            Message(plaintext).slices(MerseneTwister.N_CHARS_PER_STATE), \
                        ), mtc.p) \
                    ):
        assert len(plaintext_msg) == len(encrypted_msg) == 4
        assert Message(plaintext_msg).xor_whole(encrypted_msg).to_int() == Message(encrypted_msg).xor_whole(plaintext_msg).to_int()
        assert Message(plaintext_msg).xor_whole(encrypted_msg).xor_whole(Message().set_int(c).to_str()).to_int() == 0
        buff = Message(plaintext_msg).xor_whole(encrypted_msg).to_int()
        outputs.append(buff)
        if buff != c:
            print "For i {}; encrypted_msg {}; plaintext {}; keystream {}; encrypted_msg xor plaintext {}; encrypted_msg xor keystream {}".format(
                i,
                Message(encrypted_msg).to_int(),
                Message(plaintext_msg).to_int(),
                c,
                buff,
                Message().set_int(c).xor_whole(encrypted_msg).to_int()
            )
        if Message(encrypted_msg).xor_whole(Message().set_int(c).to_str()).to_str() != 'aaaa':
            print "--- for i {}; {} != {}".format(i, repr(encrypted_msg), c)

    # Now we get the state.
    whole_state = map(
            lambda output: int(str(get_state_from_number(Message(output).to_int()))),
            Message(encrypted_message).xor_whole(plaintext).slices(MerseneTwister.N_CHARS_PER_STATE),
        )

    for i, (a, b) in enumerate(zip(whole_state, mtc.mt.state)):
        if a != b:
            print "for i {}; {} != {}".format(i, a, b)

    print 'done'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create the MT19937 stream cipher and break it - Challenge 24 (Set 3) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

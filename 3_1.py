
import argparse
import random
from Crypto.Cipher import AES
from Crypto import Random

from lib.Message import Message
from lib.utils import get_passwd, has_correct_padding

messages = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]

def main():
    iv = Random.new().read(AES.block_size)
    c = AES.new(get_passwd(), AES.MODE_CBC, iv)

    message = Message().set_b64(random.choice(messages))
    encrypted_text = c.encrypt(message.padding().to_str())

    assert len(encrypted_text) % 16 == 0
    n_total_blocks = len(encrypted_text) / 16 + 1

    msg = ''
    encrypted_sliced = [iv] + Message(encrypted_text).all_slices(16)

    # Iterate over all blocks. We start with 1 because we target always the previous block.
    for block_index in xrange(1, n_total_blocks):

        # For each block, these are always the same.
        prefix = ''.join(encrypted_sliced[:n_total_blocks - block_index - 1])
        target = encrypted_sliced[-1-block_index]
        if block_index == 1:
            suffix = ''.join(encrypted_sliced[-block_index:])
        else:
            suffix = ''.join(encrypted_sliced[-block_index:1-block_index])

        assert len(''.join(encrypted_sliced[:n_total_blocks - block_index + 1])) == (len(prefix) + len(target) + len(suffix))

        # We store plain deciphered text for this block here.
        plain_current_block = ''

        # Iterate over all bytes of current block.
        for byte_index in xrange(16):

            # Iterate over all possible values.
            for value in reversed(range(256)):
                modified = chr(value ^ ord(target[15-byte_index]) ^ (byte_index + 1))
                for index, l in enumerate(plain_current_block):
                    modified += chr(ord(l) ^ ord(target[15-byte_index+index+1]) ^ (byte_index + 1))

                # Modified encrypted text.
                to_decrypt = prefix + target[:15-byte_index] + modified + suffix

                assert len(target) == len(target[:15-byte_index] + modified)
                assert len(to_decrypt) == (len(prefix) + len(target) + len(suffix))

                try:
                    has_correct_padding(c.decrypt(to_decrypt))
                except:
                    pass
                else:
                    plain_current_block = chr(value) + plain_current_block
                    break
            else:
                assert False, "Next letter hasn't been found"

        else:
            msg = plain_current_block + msg

    print "Message is:\n"
    print repr(msg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='The CBC padding oracle - Challenge 17 (Set 3) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

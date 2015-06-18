
import argparse
from Crypto.Cipher import AES
from Crypto import Random

from lib.Message import Message
from lib.utils import get_random_length_text, get_passwd

def set_up_text(text):
    return "comment1=cooking%20MCs;userdata=" + \
           text.replace('&', "\"&\"").replace('=', "\"=\"") + \
           ";comment2=%20like%20a%20pound%20of%20bacon"

def main():
    c = AES.new(get_passwd(), AES.MODE_CTR, counter=lambda: "\x00" * 16)
    encrypted_text = c.encrypt(Message(set_up_text('a'*16)).padding().to_str())
    target_text = Message(encrypted_text[32:48]).xor(';admin=true;a=aa').xor('a'*16).to_str()
    print "Original plain text is [{}]".format(
        repr(c.decrypt(encrypted_text))
    )
    print "Modified plain text is [{}]".format(
        repr(c.decrypt(encrypted_text[:16] + target_text + encrypted_text[32:]))
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='CTR bitflipping - Challenge 26 (Set 4) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

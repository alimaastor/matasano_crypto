
from Crypto.Cipher import AES

from lib.Message import Message
from lib.utils import get_passwd


class NonCompilantAsciiTextException(Exception):
    def __init__(self, text):
        self.text = text


def get_cypher():
    return AES.new(get_passwd(), AES.MODE_CBC, IV=get_passwd())

def check_if_high_ascii_values(text):
    try:
        text.encode("utf8")
    except UnicodeDecodeError:
        raise NonCompilantAsciiTextException(text)

def main():
    plaintext = 'a' * AES.block_size + 'b' * AES.block_size + 'c' * AES.block_size
    ciphertext = get_cypher().encrypt(plaintext)
    modified_ciphertext = \
        ciphertext[:AES.block_size] + \
        '\x00' * AES.block_size + \
        ciphertext[:AES.block_size]
    try:
        check_if_high_ascii_values(
            get_cypher().decrypt(modified_ciphertext)
        )
    except NonCompilantAsciiTextException as e:
        c1 = e.text[:AES.block_size]
        c2 = e.text[AES.block_size*2:AES.block_size*3]
        password = Message(c1).xor(c2).to_str()
        assert password == get_passwd()
        print 'password is', repr(password)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Recover the key from CBC with IV=Key - Challenge 27 (Set 4) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

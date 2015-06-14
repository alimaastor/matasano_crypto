
import argparse
from Crypto.Cipher import AES
from Crypto.Util import Counter

from lib.utils import get_passwd, get_random_text
from lib.Message import Message

IV = get_random_text(8)

def get_cypher():
    ctr_e = Counter.new(64, prefix=IV)
    return AES.new(get_passwd(), AES.MODE_CTR, counter=ctr_e)

def encrypt_messages(plain_messages):
    return map(lambda x: get_cypher().encrypt(x), plain_messages)

def get_messages():
    messages = []
    with open('data/3_4_data.txt', 'r') as f:
        for message in f:
            messages.append(message)
    return messages

def main():
    encrypted_messages = encrypt_messages(map(lambda x: Message().set_b64(x).to_str(), get_messages()))

    keystream = ''

    for encripted_chars in zip(*encrypted_messages):

        max_score = -float('inf')
        scores_and_keystream_chars = []

        for keystream_value in xrange(0,256):
            keystream_char = chr(keystream_value)
            score = Message(''.join(encripted_chars)).xor(keystream_char).score_by_char_freq()
            scores_and_keystream_chars.append((score, keystream_char))

        best_match = max(scores_and_keystream_chars, key=lambda x: x[0])
        keystream += best_match[1]

    for encrypted_message in encrypted_messages:
        print Message(encrypted_message).xor(keystream).to_str()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Break fixed-nonce CTR statistically - Challenge 20 (Set 3) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

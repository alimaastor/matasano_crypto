
import argparse
import sys
import random
from Crypto.Cipher import AES
from collections import Counter

from lib.Message import Message
from lib.MyAesCbcCypher import MyAesCbcCypher
from lib.utils import get_random_text

AES_CBC = 'AES_CBC'
AES_ECB = 'AES_ECB'

def encryption_oracle(message):
    msg = get_random_text(random.randint(5, 10)) + message + get_random_text(random.randint(5, 10))
    msg = Message(msg).padding()

    key = get_random_text()

    result = None

    if random.random() > 0.5:
        c = MyAesCbcCypher(key)
        result = (c.encrypt(msg), AES_CBC)
    else:
        c = AES.new(key, AES.MODE_ECB)
        result = (c.encrypt(msg.to_str()), AES_ECB)

    return result

def detection_oracle(message):
    best_score = -float('inf')
    for i in xrange(17):
        msg = Message(message[i:-(16-i)])
        most_common = Counter(msg.slices(4)).most_common(1)
        if most_common:
            score = Counter(msg.slices(4)).most_common(1)[0][1]
            if score > best_score:
                best_score = score
    if best_score > 2:
        return AES_ECB
    return AES_CBC

def main():
    message = 640 * 'a'
    try:
        for _ in xrange(500):
            encrypted_message, encryption_type = encryption_oracle(message)
            encryption_guessed = detection_oracle(encrypted_message)
            assert encryption_type == encryption_guessed
    except AssertionError:
        print "Detection Failed"
    else:
        print "All encryptions detected correctly"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='An ECB/CBC detection oracle - Challenge 11 (Set 2) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

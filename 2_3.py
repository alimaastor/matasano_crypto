
import sys
import random
from Crypto.Cipher import AES
from collections import Counter

from lib.Message import Message
from lib.MyAesCbcCypher import MyAesCbcCypher

AES_CBC = 'AES_CBC'
AES_ECB = 'AES_ECB'

def random_aes_key():
    r = ''
    for _ in xrange(16):
        r += chr(random.randint(0, 255))
    return r

def random_bytes():
    r = ''
    for _ in xrange(random.randint(5, 10)):
        r += chr(random.randint(0, 255))
    return r

def encryption_oracle(message):
    msg = random_bytes() + message + random_bytes()
    msg = Message(msg).padding(16)

    key = random_aes_key()
    
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

if __name__ == '__main__':
    message = 640 * 'a'
    try:
        for _ in xrange(500):
            encrypted_message, encryption_type = encryption_oracle(message)
            encryption_guessed = detection_oracle(encrypted_message)
            assert encryption_type == encryption_guessed
    except AssertException:
        print "Detection Failed"
    else:
        print "All encryptions detected correctly"

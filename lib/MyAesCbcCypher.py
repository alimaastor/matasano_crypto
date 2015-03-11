
import random
from Crypto.Cipher import AES

from lib.Message import Message


def MyAesCbcCypher(object):

    def __init__(self, password, iv=self.get_random_iv()):
        self._cypher = AES.new(password, AES.MODE_ECB)
	    self.iv = iv

    def get_random_iv(self):
        r = ''
        for _ in xrange(16):
            r += chr(random.randint(0, 255))
        return r

    def decrypt(self, msg):
        prev_ciphertext = self.iv
    	text = ''
    	for s in msg.slices(16):
	    	chunk = Message(cipher.decrypt(s)).xor(prev_ciphertext).to_str()
		    prev_ciphertext = s
    		text += chunk
	    return texta

    def encrypt(self, msg):
        prev_ciphertext = self.iv
        text = ''
        for s in msg.slices(16):

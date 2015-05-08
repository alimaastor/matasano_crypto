
import random
from Crypto.Cipher import AES

from Message import Message
from utils import get_random_text


class MyAesCbcCypher(object):

    def __init__(self, password, iv=None):
        if iv is None:
            iv = self.get_random_text()
        self._cypher = AES.new(password, AES.MODE_ECB)
        self.iv = iv

    def decrypt(self, msg):
        assert len(msg)%16 == 0
        prev_ciphertext = self.iv
        text = ''
        for s in msg.slices(16):
            chunk = Message(self._cypher.decrypt(s)).xor(prev_ciphertext).to_str()
            prev_ciphertext = s
            text += chunk
        return text

    def encrypt(self, msg):
        prev_ciphertext = self.iv
        text = ''
        for s in msg.slices(16):
            chunk = self._cypher.encrypt(Message(s).xor(prev_ciphertext).to_str())
            prev_ciphertext = chunk
            text += chunk
        return text

if __name__ == '__main__':

    import unittest

    class TestMyAesCbcCypher(unittest.TestCase):

        def test_cipher_decipher(self):
            c = MyAesCbcCypher('passwordpassword', 'YELLOW SUBMARINE')
            text = 'message message message message '
            encrypted = c.encrypt(Message(text))
            self.assertEqual(c.decrypt(Message(encrypted)), text)

        def test_cipher_decipher_no_iv(self):
            c = MyAesCbcCypher('passwordpassword', 'YELLOW SUBMARINE')
            text = 'message message message message '
            encrypted = c.encrypt(Message(text))
            self.assertEqual(c.decrypt(Message(encrypted)), text)

    unittest.main()

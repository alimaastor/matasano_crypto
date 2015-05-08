
import random
import types
from Crypto.Cipher import AES

from Message import Message
from utils import get_random_text


class MyAesCtrCypher(object):

    def __init__(self, password, iv=None):
        if iv is None:
            iv = get_random_text(7)
        else:
            assert len(iv) == 7
        self._cypher = AES.new(password, AES.MODE_ECB)
        self.iv = iv

    @staticmethod
    def ctr_to_str(ctr, iv):
        assert len(iv) == 7
        NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)
        assert isinstance(ctr, NumberTypes)

        block = ''
        buff = ctr % (256 ** 9)

        while buff / 255 != 0:
            buff, char = divmod(buff, 256)
            block = chr(char) + block
        else:
            block = chr(buff) + block

        m = (9 - len(block)) * '\x00' + block + iv
        assert len(m) == 16

        return m

    def encrypt(self, msg):
        message = ''
        m = Message(msg)
        for ctr, s in enumerate(m.slices(16)):
            chunk = Message(self._cypher.encrypt(MyAesCtrCypher.ctr_to_str(ctr, self.iv)))
            text = Message(chunk[:len(s)]).xor(s).to_str()
            message += text
        assert len(message) == len(msg)
        return message

    def decrypt(self, msg):
        return self.encrypt(msg)


if __name__ == '__main__':

    import unittest

    class TestMyAesCtrCypher(unittest.TestCase):

        def test_cipher_decipher(self):
            c = MyAesCtrCypher('passwordpassword', '1234567')
            text = 'message message message message '
            self.assertEqual(c.encrypt(c.decrypt(text)), text)

    unittest.main()

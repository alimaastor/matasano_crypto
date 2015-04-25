
import random
from Crypto.Cipher import AES

from Message import Message
from utils import static_var

@static_var('passwd', reduce(lambda x,_: x + chr(random.randint(0,255)),xrange(16),''))
def get_passwd():
    return get_passwd.passwd

def has_correct_padding(txt):
    to_check = txt
    last_byte_number = ord(to_check[-1])
    if last_byte_number == 1:
        return True
    is_ok = True
    if to_check[-last_byte_number:-1] == to_check[-last_byte_number+1:]:
        return True
    raise ValueError()

class Cypher(object):
    def __init__(self, password=get_passwd()):
        self._cypher = AES.new(password, AES.MODE_ECB)

    def encrypt(self, txt):
        msg = Message(txt).padding(16)
        return self._cypher.encrypt(msg.to_str())

    def decrypt(self, txt):
        return self._cypher.decrypt(txt)

if __name__ == '__main__':

    import unittest

    class TestCypherClass(unittest.TestCase):

        def test_encrypt_decrypt(self):
            c = Cypher('aaaaaaaaaaaaaaaa')
            text = 'abcdefghijklmnop'
            self.assertEqual(c.decrypt(c.encrypt(text)), text)

        def test_password(self):
            self.assertEqual(len(get_passwd()), 16)

        def test_has_correct_padding(self):
            self.assertTrue(has_correct_padding('ICE ICE BABY\x04\x04\x04\x04'))
            self.assertTrue(has_correct_padding('ICE ICE BABY\x04\x04\x04\x01'))
            self.assertTrue(has_correct_padding('aaaaaaaaaaaaaaa\x01'))
            self.assertTrue(has_correct_padding('ICE ICE BABYaa\x02\x02'))
            self.assertRaises(ValueError, has_correct_padding, 'ICE ICE BABY\x05\x05\x05\x05')
            self.assertRaises(ValueError, has_correct_padding, "ICE ICE BABY\x01\x02\x03\x04")

    unittest.main()

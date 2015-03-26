
import random
from Crypto.Cipher import AES

from Message import Message
from utils import static_var

@static_var('passwd', reduce(lambda x,_: x + chr(random.randint(0,255)),xrange(16),''))
def get_passwd():
    return get_passwd.passwd

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

    unittest.main()

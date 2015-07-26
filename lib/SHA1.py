
import struct
import copy

import struct

from Message import Message

def leftrotate(i, n):
    return ((i << n) & 0xffffffff) | (i >> (32 - n))

class SHA1(object):
    '''Copied from https://gist.github.com/bonsaiviking/5639034'''

    @staticmethod
    def state_from_str_result(str_msg):
        assert len(str_msg) == 20
        r = []
        for chunk in [str_msg[i:i+4] for i in xrange(0, 20, 4)]:
            result = ''
            for char in chunk:
                hex_char = format(ord(char), "01x")
                if len(hex_char) % 2 != 0:
                    hex_char = '0' + hex_char
                result += hex_char
            r.append(int(result, 16))
        return r

    @staticmethod
    def state_from_hex_result(hex_msg):
        assert len(hex_msg) == 40
        return [int(hex_msg[i:i+8], 16) for i in xrange(0, 40, 8)]

    def __init__(self, data='', h0=0x67452301, h1=0xEFCDAB89, h2=0x98BADCFE, h3=0x10325476, h4=0xC3D2E1F0):
        self.h = [h0, h1, h2, h3, h4]
        self.remainder = data
        self.count = 0

    def _add_chunk(self, chunk):
        self.count += 1
        w = list( struct.unpack(">16I", chunk) + (None,) * (80-16) )
        for i in xrange(16, 80):
            n = w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]
            w[i] = leftrotate(n, 1)
        a,b,c,d,e = self.h
        for i in xrange(80):
            f = None
            k = None
            if i < 20:
                f = (b & c) ^ (~b & d)
                k = 0x5A827999
            elif i < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif i < 60:
                f = (b & c) ^ (b & d) ^ (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (leftrotate(a,5) + f + e + k + w[i]) % 2**32
            e = d
            d = c
            c = leftrotate(b, 30)
            b = a
            a = temp
        self.h[0] = (self.h[0] + a) % 2**32
        self.h[1] = (self.h[1] + b) % 2**32
        self.h[2] = (self.h[2] + c) % 2**32
        self.h[3] = (self.h[3] + d) % 2**32
        self.h[4] = (self.h[4] + e) % 2**32

    def add(self, data):
        message = self.remainder + data
        r = len(message) % 64
        if r != 0:
            self.remainder = message[-r:]
        else:
            self.remainder = ""
        for chunk in xrange(0, len(message)-r, 64):
            self._add_chunk( message[chunk:chunk+64] )
        return self

    def finish(self):
        l = len(self.remainder) + 64 * self.count
        self.add( "\x80" + "\x00" * ((55 - l) % 64) + struct.pack(">Q", l * 8) )
        h = tuple(x for x in self.h)
        self.__init__()
        return struct.pack(">5I", *h)


if __name__ == '__main__':

    import unittest

    class TestMessageClass(unittest.TestCase):

        def test_simple_digest(self):
            import hashlib
            text = 'aaaaaaaaaaaaaaaaa'

            sha1 = SHA1()
            sha1.add(text)
            my_msg = sha1.finish()

            d = hashlib.sha1()
            d.update(text)
            correct_msg = d.digest()

            self.assertEqual(my_msg, correct_msg)

        def test_multiple_update(self):
            import hashlib
            text = 'aaaaaaaaaaaaaaaaa'

            sha1 = SHA1()
            sha1.add(text)
            sha1.add(text)
            my_msg = sha1.finish()

            d = hashlib.sha1()
            d.update(text)
            d.update(text)
            correct_msg = d.digest()

            self.assertEqual(my_msg, correct_msg, 'second digest, {} != {}'.format(repr(my_msg), repr(correct_msg)))

        def test_from_prevously_hashed_result(self):
            import hashlib
            text = 'aaaaaaaaaaaaaaaaa'

            d = hashlib.sha1()
            d.update(text)
            previous_msg = d.digest()

            h0, h1, h2, h3, h4 = SHA1.state_from_str_result(previous_msg)
            sha1 = SHA1(text, h0, h1, h2, h3, h4)
            my_msg = sha1.finish()

            d = hashlib.sha1()
            d.update(text)
            d.update(text)
            correct_msg = d.digest()

            self.assertEqual(my_msg, correct_msg, 'second digest, {} != {}'.format(repr(my_msg), repr(correct_msg)))

    unittest.main()

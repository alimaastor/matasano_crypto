
import pdb

import types
from collections import Counter
from itertools import combinations

class Message(object):

    char_freq = {
        'a': 0.0651738,
        'b': 0.0124248,
        'c': 0.0217339,
        'd': 0.0349835,
        'e': 0.1041442,
        'f': 0.0197881,
        'g': 0.0158610,
        'h': 0.0492888,
        'i': 0.0558094,
        'j': 0.0009033,
        'k': 0.0050529,
        'l': 0.0331490,
        'm': 0.0202124,
        'n': 0.0564513,
        'o': 0.0596302,
        'p': 0.0137645,
        'q': 0.0008606,
        'r': 0.0497563,
        's': 0.0515760,
        't': 0.0729357,
        'u': 0.0225134,
        'v': 0.0082903,
        'w': 0.0171272,
        'x': 0.0013692,
        'y': 0.0145984,
        'z': 0.0007836,
        ' ': 0.1918182,
    }

    def __init__(self, msg=''):
        if isinstance(msg, Message):
            self._message = msg.to_str()
        else:
            assert isinstance(msg, str)
            self._message = msg

    def to_bin(self):
        result = ''
        for char in self._message:
            bin_char = bin(ord(char))[2:]
            bin_char = (8-len(bin_char))*'0' + bin_char
            result += bin_char
        return result

    def to_hex(self):
        result = ''
        for char in self._message:
            hex_char = format(ord(char), "01x")
            if len(hex_char) % 2 != 0:
                hex_char = '0' + hex_char
            result += hex_char
        return result

    def to_b64(self):
        return self._message.encode('base64').replace('\n', '')

    def to_int(self):
        return int(self.to_hex(), 16)

    def to_str(self):
        return self._message

    def set_hex(self, hex_number):
        assert isinstance(hex_number, str)
        if len(hex_number)%2 != 0:
            hex_number = '0' + hex_number
        self._message = ''.join([chr(int(char1+char2, 16))
            for char1, char2 in zip(hex_number[0::2], hex_number[1::2])])
        return self

    def set_str(self, string):
        assert isinstance(string, str)
        self._message = string
        return self

    def set_bin(self, bin_number):
        assert isinstance(bin_number, str)
        self.set_int(int(bin_number, 2))
        return self

    def set_b64(self, b64_number):
        assert isinstance(b64_number, str)
        self._message = b64_number.decode('base64')
        return self

    def set_int(self, number):
        NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)
        assert isinstance(number, NumberTypes)
        self.set_hex(format(number, '01x'))
        return self

    def distance_to(self, other_msg):
        if isinstance(other_msg, str):
            other = Message(other_msg)
        else:
            assert isinstance(other_msg, Message)
            other = other_msg
        if len(self) != len(other):
            raise ValueError("Undefined for sequences of unequal length")
        return sum(ch1 != ch2 for ch1, ch2 in zip(self.to_bin(), other.to_bin()))

    def normalized_distance_to(self, other_msg):
        return self.distance_to(other_msg) * 1.0 / len(self)

    def xor(self, key, extend_key=True):
        if extend_key:
            quotient, remainder = divmod(len(self._message), len(key))
            extended_key = quotient * key + key[:remainder]
        else:
            if len(self._message) > len(key):
                extended_key = '\x00' * (len(self._message) - len(key)) + key
            elif len(self._message) < len(key):
                extended_key = key
                self._message = '\x00' * (len(key) - len(self._message)) + self._message
            elif len(self._message) == len(key):
                extended_key = key
            else:
                assert False, "Not possible"

        result = ''
        for msg_char, key_char in zip(*[self._message, extended_key]):
            ciphered_char = chr(ord(msg_char) ^ ord(key_char))
            result += ciphered_char
        self._message = result
        return self

    def xor_whole(self, key):
        return self.xor(key, extend_key=False)

    def score(self):
        msg = self._message
        if not msg:
            return -float('inf')
        char_count = Counter(msg.upper()).most_common()
        char_freq = [x for x, _ in char_count]
        if len(char_freq) < 10:
            return -float('inf')
        score = 0
        most_common = char_freq[:5]
        if ' ' == most_common[0]:
            score += 5
        for letter in most_common:
            if letter in 'EATOIN':
                score += 1
        least_common = char_freq[:-5]
        for letter in least_common:
            if letter in 'KJXQZ':
                score += 1
        return score

    def score_by_char_freq(self):
        return sum(Message.char_freq[c] for c in self._message.lower() if c in Message.char_freq)

    def get_block_sizes(self, n_sizes=10, n_average_blocks=5):
        sizes = []
        n_blocks = min(len(self)/2, 40)
        for size in xrange(1,n_blocks):

            blocks = [self[i:i+size] for i in xrange(0, min(n_average_blocks*size, len(self) - len(self)%size), size)]
            distances = [Message(b1).normalized_distance_to(b2) for b1, b2 in combinations(blocks[:n_average_blocks], 2)]
            size_score = sum(distances)/float(len(distances))
            sizes.append((size_score, size))
        sizes.sort()
        return [s for _, s in sizes[:n_sizes]]

    def padding(self, block_length=16):
        n_bytes = block_length - (len(self._message) % block_length)
        if n_bytes == block_length:
            return self
        assert n_bytes >= 0
        self._message += n_bytes * chr(n_bytes)
        assert len(self) % block_length == 0
        return self

    def slices(self, slice_size=2):
        n_whole_chunks = len(self._message) / slice_size
        assert n_whole_chunks <= len(self._message)
        for i in xrange(0, n_whole_chunks * slice_size, slice_size):
            buff = ''
            for a in xrange(slice_size):
                buff += self._message[i+a]
            yield buff
        if n_whole_chunks < len(self._message) / slice_size:
            yield self._message[n_whole_chunks * slice_size:]

    def all_slices(self, slice_size=2):
        r = []
        for e in self.slices(slice_size):
            r.append(e)
        return r

    def __eq__(self, other):
        if isinstance(other, str):
            return self._message == other
        if isinstance(other, Message):
            return self._message == other.to_str()
        return False

    def __len__(self):
        return len(self._message)

    def __getitem__(self, key):
        return self._message[key]

    def __setitem__(self, key, value):
        self._message[key] = value

    def __str__(self):
        return repr(self._message)

    def __repr__(self):
        return repr(self._message)


if __name__ == '__main__':

    import unittest

    class TestMessageClass(unittest.TestCase):

        def setUp(self):
            self.message = Message('012345')

        def test_to_str(self):
            self.assertEqual(self.message.to_str(), '012345')

        def test_to_bin(self):
            self.assertEqual(self.message.to_bin(), '001100000011000100110010001100110011010000110101')

        def test_to_hex(self):
            self.assertEqual(self.message.to_hex(), '303132333435')

        def test_to_int(self):
            self.assertEqual(self.message.to_int(), 52987853747253)
            for i in xrange(10000):
                m = Message().set_int(i).to_hex()
                self.assertEqual(Message().set_hex(m).to_int(), i)

        def test_to_b64(self):
            self.assertEqual(self.message.to_b64(), 'MDEyMzQ1')

        def test_set_hex(self):
            message = Message()
            message.set_hex('303132333435')
            self.assertEqual(message.to_str(), '012345')

        def test_set_int(self):
            message = Message()
            message.set_int(52987853747253)
            self.assertEqual(message.to_str(), '012345')

        def test_set_str(self):
            message = Message()
            message.set_str('012345')
            self.assertEqual(message.to_str(), '012345')

        def test_set_bin(self):
            message = Message()
            message.set_bin('001100000011000100110010001100110011010000110101')
            self.assertEqual(message.to_str(), '012345')

        def test_set_b64(self):
            message = Message()
            message.set_b64('MDEyMzQ1')
            self.assertEqual(message.to_str(), '012345')

        def test_distance_to(self):
            self.assertEqual(Message('this is a test').distance_to('wokka wokka!!!'), 37)

        def test_normalized_distance_to(self):
            self.assertEqual(Message('this is a test').normalized_distance_to('wokka wokka!!!'), 37./14)

        def test_equal(self):
            self.assertEqual(Message('this is a test'), 'this is a test')
            self.assertEqual(Message('this is a test'), Message('this is a test'))
            self.assertNotEqual(Message('this is a test'), 123)

        def test_xor(self):
            msg = 'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'
            message = Message(msg)
            message.xor('ICE')
            self.assertEqual(message.to_hex(), '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226'
                                               '324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20'
                                               '283165286326302e27282f')

            for i in xrange(10000):
                m = Message().set_int(i).xor(Message().set_int(1234).to_str()).to_int()
                self.assertEqual(m, i ^ 1234, "i = {}".format(i))

        def test_padding(self):
            self.assertEqual(Message("YELLOW SUBMARINE").padding(20), "YELLOW SUBMARINE\x04\x04\x04\x04")
            self.assertEqual(Message("aaaaaaaaaaaaaaa").padding(16), "aaaaaaaaaaaaaaa\x01")
            self.assertEqual(Message("aaaaaaaaaaaaaa").padding(16), "aaaaaaaaaaaaaa\x02\x02")
            self.assertEqual(Message("aaaaaaaaaaaaa").padding(16), "aaaaaaaaaaaaa\x03\x03\x03")
            self.assertEqual(Message("aaaaaaaaaaaa").padding(16), "aaaaaaaaaaaa\x04\x04\x04\x04")
            self.assertEqual(Message("aaaaaaaaaaa").padding(16), "aaaaaaaaaaa\x05\x05\x05\x05\x05")
            self.assertEqual(Message("aaaaaaaaaa").padding(16), "aaaaaaaaaa\x06\x06\x06\x06\x06\x06")
            self.assertEqual(Message("aaaaaaaaa").padding(16), "aaaaaaaaa\x07\x07\x07\x07\x07\x07\x07")
            self.assertEqual(Message("aaaaaaaa").padding(16), "aaaaaaaa\x08\x08\x08\x08\x08\x08\x08\x08")
            self.assertEqual(Message("aaaaaaa").padding(16), "aaaaaaa\x09\x09\x09\x09\x09\x09\x09\x09\x09")
            self.assertEqual(Message("aaaaaa").padding(16), "aaaaaa\x0A\x0A\x0A\x0A\x0A\x0A\x0A\x0A\x0A\x0A")
            self.assertEqual(Message("aaaaa").padding(16), "aaaaa\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B")
            self.assertEqual(Message("aaaa").padding(16), "aaaa\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C")
            self.assertEqual(Message("aaa").padding(16), "aaa\x0D\x0D\x0D\x0D\x0D\x0D\x0D\x0D\x0D\x0D\x0D\x0D\x0D")
            self.assertEqual(Message("aa").padding(16), "aa\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E")
            self.assertEqual(Message("a").padding(16), "a\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F\x0F")

    unittest.main()

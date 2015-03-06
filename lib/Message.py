
import types
from collections import Counter
from itertools import combinations

class Message(object):

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

    def cipher(self, key):
        # assert isinstance(key, str)
        quotient, remainder = divmod(len(self), len(key))
        extended_key = quotient * key + key[:remainder]

        result = ''
        for msg_char, key_char in zip(*[self._message, extended_key]):
            ciphered_char = chr(ord(msg_char) ^ ord(key_char))
            result += ciphered_char
        self._message = result
        return self

    def decipher(self, key):
        return self.cipher(key)

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
        return self._message

    def __repr__(self):
        return self._message


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

        def test_cipher(self):
            msg = 'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'
            message = Message(msg)
            message.cipher('ICE')
            self.assertEqual(message.to_hex(), '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226'
                                               '324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20'
                                               '283165286326302e27282f')
            message.decipher('ICE')
            self.assertEqual(message.to_str(), msg)

        # def test_score(self):
        #     self.assertEqual(Message('1234abcd__--;;').score(), 8)

    unittest.main()

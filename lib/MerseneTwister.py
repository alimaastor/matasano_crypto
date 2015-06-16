

class MerseneTwister(object):

    STATE_LENGTH = 624
    _seed = None

    '''
     // Create a length 624 array to store the state of the generator
     int[0..623] MT
     int index = 0
    '''
    def __init__(self, seed=None):
        self.reset_internal_state()
        if seed:
            self._seed = seed
            self.initialise_generator(seed)

    def reset_internal_state(self):
        self.state = [0] * MerseneTwister.STATE_LENGTH
        self.index = 0

    '''
     // Initialize the generator from a seed
     function initialize_generator(int seed) {
         index := 0
         MT[0] := seed
         for i from 1 to 623 { // loop over each element
             MT[i] := lowest 32 bits of(1812433253 * (MT[i-1] xor (right shift by 30 bits(MT[i-1]))) + i) // 0x6c078965
         }
     }
    '''
    def initialise_generator(self, seed):
        assert isinstance(seed, int)
        self.reset_internal_state()
        self._seed = seed
        self.state[0] = seed
        for i in xrange(1,MerseneTwister.STATE_LENGTH):
            self.state[i] = \
                (1812433253 * \
                    (self.state[i - 1] ^ \
                        (self.state[i - 1] >> 30)\
                    ) + i \
                ) & 0xffffffff

    '''
     // Extract a tempered pseudorandom number based on the index-th value,
     // calling generate_numbers() every 624 numbers
     function extract_number() {
         if index == 0 {
             generate_numbers()
         }

         int y := MT[index]
         y := y xor (right shift by 11 bits(y))
         y := y xor (left shift by 7 bits(y) and (2636928640)) // 0x9d2c5680
         y := y xor (left shift by 15 bits(y) and (4022730752)) // 0xefc60000
         y := y xor (right shift by 18 bits(y))

         index := (index + 1) mod 624
         return y
     }
    '''
    def extract_number(self):
        if self.index == 0:
            self.generate_numbers()

        y  = self.state[self.index]
        y ^=   (y >> 11)
        y ^= ( (y <<  7) & (2636928640) )
        y ^= ( (y << 15) & (4022730752) )
        y ^=   (y >> 18)

        self.index += 1
        self.index %= MerseneTwister.STATE_LENGTH

        return y

    '''
     // Generate an array of 624 untempered numbers
     function generate_numbers() {
         for i from 0 to 623 {
             int y := (MT[i] and 0x80000000)                       // bit 31 (32nd bit) of MT[i]
                            + (MT[(i+1) mod 624] and 0x7fffffff)   // bits 0-30 (first 31 bits) of MT[...]
             MT[i] := MT[(i + 397) mod 624] xor (right shift by 1 bit(y))
             if (y mod 2) != 0 { // y is odd
                 MT[i] := MT[i] xor (2567483615) // 0x9908b0df
             }
         }
     }
     '''
    def generate_numbers(self):
        for i in xrange(MerseneTwister.STATE_LENGTH):
            y = (self.state[i] & 0x80000000) + ((self.state[(i + 1) % MerseneTwister.STATE_LENGTH]) & 0x7fffffff)
            self.state[i] = self.state[(i + 397) % MerseneTwister.STATE_LENGTH] ^ (y >> 1)
            if y % 2 == 0:
                self.state[i] ^= 2567483615


def get_state_from_number(number):
    # y  = self.state[self.index]
    # y ^=   (y >> 11)
    # y ^= ( (y <<  7) & (2636928640) )
    # y ^= ( (y << 15) & (4022730752) )
    # y ^=   (y >> 18)

    return None

if __name__ == '__main__':

    import unittest

    class TestMersenneTwister(unittest.TestCase):

        def test_set_up(self):
            mt = MerseneTwister()
            self.assertEqual(len(mt.state), MerseneTwister.STATE_LENGTH)
            self.assertEqual(mt.state, [0] * MerseneTwister.STATE_LENGTH)
            self.assertEqual(mt._seed, None)
            seed = 1234
            mt.initialise_generator(seed)
            self.assertNotEqual(mt.state, [0] * MerseneTwister.STATE_LENGTH)
            self.assertEqual(len(mt.state), MerseneTwister.STATE_LENGTH)
            self.assertEqual(mt._seed, seed)

        def test_set_up_with_seed(self):
            seed = 1234
            mt = MerseneTwister(seed)
            self.assertEqual(len(mt.state), MerseneTwister.STATE_LENGTH)
            self.assertNotEqual(mt.state, [0] * MerseneTwister.STATE_LENGTH)
            self.assertEqual(mt._seed, seed)

        def test_regenerates_state(self):
            import copy
            seed = 1234
            mt = MerseneTwister(seed)
            previous_state = copy.deepcopy(mt.state)
            for _ in xrange(MerseneTwister.STATE_LENGTH): mt.generate_numbers()
            next_state = mt.state
            self.assertNotEqual(previous_state, next_state)

    unittest.main()

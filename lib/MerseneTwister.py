
class MerseneTwister(object):
    '''
     // Create a length 624 array to store the state of the generator
     int[0..623] MT
     int index = 0
    '''
    state = [0] * 625
    index = 0

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
    @staticmethod
    def initialise_generator(seed):
        MerseneTwister.state[0] = seed
        for i in xrange(1,625):
            MerseneTwister.state[i] = \
                (1812433253 * \
                    (MerseneTwister.state[i - 1] ^ \
                        (MerseneTwister.state[i - 1] >> 30)\
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
    @staticmethod
    def extract_number():
        if MerseneTwister.index == 0:
            MerseneTwister.generate_numbers()

        y  = MerseneTwister.state[MerseneTwister.index]
        y ^=   (y >> 11)
        y ^= ( (y <<  7) & (2636928640) )
        y ^= ( (y << 15) & (4022730752) )
        y ^=   (y >> 18)

        MerseneTwister.index += 1
        MerseneTwister.index %= 624

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
    @staticmethod
    def generate_numbers():
        for i in xrange(623):
            y = (MerseneTwister.state[i] & 0x80000000) + ((MerseneTwister.state[i + 1] % 624) & 0x7fffffff)
            MerseneTwister.state[i] = MerseneTwister.state[(i + 397) % 624] ^ (y >> 1)
            if y % 2 == 0:
                MerseneTwister.state[i] ^= 2567483615

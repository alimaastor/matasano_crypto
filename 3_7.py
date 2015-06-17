
import argparse

from lib.MerseneTwister import MerseneTwister, get_state_from_number

def main():
    seed = 5489
    mt = MerseneTwister(seed)

    states = map(
      lambda _: get_state_from_number(mt.extract_number()),
      xrange(MerseneTwister.STATE_LENGTH)
    )

    assert len(states) == MerseneTwister.STATE_LENGTH

    mt_clone = MerseneTwister()
    mt_clone.set_state_and_index(states, 0)

    for _ in xrange(1000000):
        assert mt_clone.extract_number() == mt.extract_number()
    else:
        print "Mersene Twister PRNG cloned correctly."

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Clone an MT19937 RNG from its output - Challenge 23 (Set 3) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

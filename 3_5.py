
import argparse

from lib.MerseneTwister import MerseneTwister

def main():
    seed = 5489
    print 'Using seed', seed, '\n'
    mt = MerseneTwister()
    mt.initialise_generator(seed)

    print 'Random numbers:'
    for _ in range(1000):
        print mt.extract_number()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Implement the MT19937 Mersenne Twister RNG - Challenge 21 (Set 3) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

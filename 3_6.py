
import argparse
import time
import random

from lib.MerseneTwister import MerseneTwister

def main():
    seconds = random.randrange(40, 1000)
    print "waiting", seconds, "seconds"
    time.sleep(seconds)
    seed = int(time.time())
    print "seed is", seed
    mt = MerseneTwister(seed)
    seconds = random.randrange(40, 1000)
    print "waiting", seconds, "seconds"
    time.sleep(seconds)
    first_value = mt.extract_number()

    current_time = int(time.time())
    print "current time", current_time
    for i in xrange(1000):
        new_seed = current_time - i
        mt2 = MerseneTwister(new_seed)
        if mt2.extract_number() == first_value:
            print "seed was", new_seed
            break
    else:
        print "Seed not found"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Crack an MT19937 seed - Challenge 22 (Set 3) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

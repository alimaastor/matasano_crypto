
import argparse
import os
import json
from collections import Counter

from lib.Message import Message

def main():
    results = []
    with open(os.path.join("data", "1_8_data.txt"), 'r') as f:
        for linenumber, line in enumerate(f):
            line = line.strip()
            assert len(line)%4==0
            counter = Counter()
            for a, b, c, d in zip(line[0::4], line[1::4], line[2::4], line[3::4]):
                counter.update([a + b + c + d])
            results.append([counter.most_common(), line, linenumber])
        results.sort(key=lambda x: x[0][0][1])
    print "Line is [{}] and line number is [{}]".format(results[-1][1], results[-1][2])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Detect AES in ECB mode - Challenge 8 (Set 1) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

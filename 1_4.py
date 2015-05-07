
import os
import argparse

from lib.Message import Message

def score_string(string):
    '''This score function is slightly different to the one used in Message.py
    because we don't use letter frequency analysis here.'''
    score = 0
    for char in string:
        if char == " ":
            score += 5
        elif char.isalnum() or char in "',.":
            score += 1
    return score

def main():
    best_score = -1
    with open(os.path.join("data", "1_4_data.txt"), 'r') as f:
        for line_number, line in enumerate(f):
            for i in xrange(256):
                key = chr(i)
                message = Message().set_hex(line.replace('\n','')).xor(key).to_str()
                score = score_string(message)
                if score > best_score:
                    best_score = score
                    result = (message.replace('\n',''), key, line_number, score)

    print "Line is [{}] (key = [{}]; line number = [{}], score = [{}])".format(*result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Single-byte XOR cipher - Challenge 3 (Set 1) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

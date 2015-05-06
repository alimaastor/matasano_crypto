
import argparse

def xor(n1, n2):
    return format(n1 ^ n2, "01x")

def parse_number(number):
    try:
        n = int(number, 16)
    except ValueError:
        print "Hexadecimal number [{}] does not have a valid format.".format(number)
        exit(1)
    else:
        return n

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Fixed XOR - Challenge 2 (Set 1) of Matasano Crypto Challenge.')
    parser.add_argument('hex_number1',
        help='First hexadecimal number to be XOR\'d', type=str)
    parser.add_argument('hex_number2',
        help='Second hexadecimal number to be XOR\'d', type=str)

    args = parser.parse_args()

    if len(args.hex_number1) != len(args.hex_number2):
        print "Length of numbers [{}] and [{}] are not equal.".format(
            args.hex_number1,
            args.hex_number2)
        exit(1)

    print "[{}] ^ [{}] = [{}]".format(
        args.hex_number1,
        args.hex_number2,
        xor(parse_number(args.hex_number1), parse_number(args.hex_number2)))

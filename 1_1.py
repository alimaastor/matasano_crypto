
import argparse

def hex2base64(hex_number):
	result = ''
	quotient = hex_number
	while quotient > 0:
		quotient, remainder = divmod(quotient, 64)
		result = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'[remainder] + result
	return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert hex to base64 - Challenge 1 (Set 1) of Matasano Crypto Challenge.')
    parser.add_argument('hex_number',
        help='hexadecimal number to be converted to Base64', type=str)

    args = parser.parse_args()

    try:
    	hex_number = int(args.hex_number, 16)
    except ValueError:
    	print "Hexadecimal number [{}] does not have a valid format.".format(args.hex_number)
    	exit(1)
    else:
    	print "Base64 representation of hexadecimal number [{}] is [{}]".format(args.hex_number, hex2base64(hex_number))

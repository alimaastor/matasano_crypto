
def cipher(message, key):
	result = ''
	for msg_char, key_char in zip(*[message, key]):
		ciphered_char = ord(msg_char) ^ ord(key_char)
		result += format(ciphered_char, "01x")
	if len(result)%2 != 0:
		result = '0' + result
	return result

def cipher_message(message, key):
	quotient, remainder = divmod(len(message), len(key))
	extended_key = quotient * key + key[:remainder]
	return cipher(message, extended_key)

if __name__ == '__main__':
	import sys
	print cipher_message(sys.argv[1], sys.argv[2])

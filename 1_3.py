from Message import Message
import sys

if __name__ == '__main__':

	result = []

	for i in xrange(256):
		key = chr(i)
		message = Message().set_hex(sys.argv[1]).decipher(key)
		score = message.score()
		result.append((score, message, key))

	result.sort(reverse=True)

	for r in result:
		print r


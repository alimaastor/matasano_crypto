
import sys
import random

def random_aes_key():
	r = ''
	for _ in xrange(16):
		r += chr(random.randint(0,255))
	return r

def encryption_oracle(message):
	key = random_aes_key()
	if random.random() > 0.5:
		# AES CBC
		pass
	else:
		#AES ECB
		pass

if __name__ == '__main__':
	print random_aes_key()

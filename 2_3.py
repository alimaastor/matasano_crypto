
import sys
import random

def random_aes_key():
	r = ''
	for _ in xrange(16):
		r += chr(random.randint(0, 255))
	return r

def random_bytes():
    r = ''
    for _ in random.randint(5, 10):
        r += chr(random.randint(0, 255))
    return r

def encryption_oracle(message):
	key = random_aes_key()
    msg = random_bytes() + message + random_bytes()
	if random.random() > 0.5:
		# AES CBC
		pass
	else:
		#AES ECB
		pass

if __name__ == '__main__':
	print random_aes_key()

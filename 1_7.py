
import sys
from Crypto.Cipher import AES

if __name__ == '__main__':
	cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
	with open(sys.argv[1], 'r') as f:
		print cipher.decrypt(f.read().decode('base64'))

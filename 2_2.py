
import sys
from Crypto.Cipher import AES

from lib.Message import Message

if __name__ == '__main__':
	cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
	with open(sys.argv[1], 'r') as f:
		msg = Message().set_b64(f.read())
	iv = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	prev_ciphertext = iv
	text = ''
	for s in msg.slices(16):
		chunk = Message(cipher.decrypt(s)).xor(prev_ciphertext).to_str()
		prev_ciphertext = s
		text += chunk
	print text

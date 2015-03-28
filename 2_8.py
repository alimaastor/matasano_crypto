
from Crypto.Cipher import AES
from Crypto import Random

from lib.Message import Message
from lib.Cypher import get_passwd
from lib.utils import get_random_length_text

def set_up_text(text):
	return "comment1=cooking%20MCs;userdata=" + \
		   text.replace('&', "\"&\"").replace('=', "\"=\"") + \
		   ";comment2=%20like%20a%20pound%20of%20bacon"

if __name__ == '__main__':
	c = AES.new(get_passwd(), AES.MODE_CBC, Random.new().read(AES.block_size))
	encrypted_text = c.encrypt(Message(set_up_text('a'*16)).padding().to_str())
	target_text = Message(encrypted_text[16:32]).xor(';admin=true;a=aa').xor('a'*16).to_str()
	print c.decrypt(encrypted_text)
	print c.decrypt(encrypted_text[:16] + target_text + encrypted_text[32:])


import argparse
import os
from Crypto.Cipher import AES

from lib.Message import Message

def main():
    cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
    with open(os.path.join("data", "2_2_data.txt"), 'r') as f:
        msg = Message().set_b64(f.read())
    iv = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    prev_ciphertext = iv
    text = ''
    for s in msg.slices(16):
        chunk = Message(cipher.decrypt(s)).xor(prev_ciphertext).to_str()
        prev_ciphertext = s
        text += chunk
    print "Message is:\n"
    print text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Implement CBC mode - Challenge 10 (Set 2) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()
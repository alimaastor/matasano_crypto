
import argparse
import os
from Crypto.Cipher import AES

def main():
    cipher = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
    with open(os.path.join("data", "1_7_data.txt"), 'r') as f:
        print "Deciphered text is:\n"
        print cipher.decrypt(f.read().decode('base64'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='AES in ECB mode - Challenge 7 (Set 1) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

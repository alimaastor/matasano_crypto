
import argparse

from lib.utils import has_correct_padding

def main():
    if not has_correct_padding('ICE ICE BABY\x04\x04\x04\x04'):
        print 'error'
        exit()
    try:
        has_correct_padding('ICE ICE BABY\x05\x05\x05\x05')
    except ValueError:
        pass
    else:
        print 'error'
        exit()
    try:
        has_correct_padding("ICE ICE BABY\x01\x02\x03\x04")
    except ValueError:
        pass
    else:
        print 'error'
        exit()
    print 'ok'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PKCS#7 padding validation - Challenge 15 (Set 2) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()

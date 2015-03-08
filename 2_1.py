
import sys

from lib.Message import Message

if __name__ == '__main__':
	print Message(sys.argv[1]).padding(block_length=20)

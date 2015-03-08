
import sys
import json
from collections import Counter

from lib.Message import Message

if __name__ == '__main__':
	results = []
	with open(sys.argv[1], 'r') as f:
		for linenumber, line in enumerate(f):
			line = line.strip()
			assert len(line)%4==0
			counter = Counter()
			for a, b, c, d in zip(line[0::4], line[1::4], line[2::4], line[3::4]):
				counter.update([a + b + c + d])
			results.append([counter.most_common(), line, linenumber])
		results.sort(key=lambda x: x[0][0][1])
	print results[-1]

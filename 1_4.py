
def decipher(hex_number, hex_char):
	assert hex_number
	assert hex_char
	if len(hex_number)%2 == 1:
		hex_number = '0' + hex_number
	if len(hex_char)%2 == 1:
		hex_char = '0' + hex_char
	assert len(hex_number)%len(hex_char) == 0
	hex_char = len(hex_number)/len(hex_char) * hex_char
	r = format(int(hex_number, 16) ^ int(hex_char, 16), "01x")
	result = ''
	for char1, char2 in zip(r[0::2], r[1::2]):
		try:
			if int(char1+char2, 16) > 128:
				return ""
			char = chr(int(char1+char2, 16))
			if len(char) > 1:
				return ""
			result = result + char
		except UnicodeEncodeError:
			return ""
	return result

def score_string(string):
	score = 0
	for char in string:
		if char.isalnum() or char in "' ,.":
			score += 1
	return score

if __name__ == '__main__':
	import sys
	with open(sys.argv[1], 'r') as f:
		best_result = [(0, '', '')]
		for line_number, line in enumerate(f):
			result = []

			for i in xrange(256):
				key = format(i, "01x")
				message = decipher(line, key)
				if not message:
					continue
				score = score_string(message)
				result.append((score, message, key, line, line_number))

			result.sort(reverse=True)

			if result and result[0] > best_result:
				best_result = result[0]
	print best_result
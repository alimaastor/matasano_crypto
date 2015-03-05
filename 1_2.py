
def xor(n1, n2):
	if not isinstance(n1, int):
		number1 = int(n1, 16)
	else:
		number1 = n1
	if not isinstance(n2, int):
		number2 = int(n2, 16)
	else:
		number2 = n2
	return format(number1 ^ number2, "01x")

if __name__ == '__main__':
	import sys
	print xor(sys.argv[1], sys.argv[2])


def hex2base64(hex_number):
	if not isinstance(hex_number, int):
		quotient = int(hex_number, 16)
	else:
		quotient = hex_number
		
	result = ''
	while quotient > 0:
		quotient, remainder = divmod(quotient, 64)
		result = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'[remainder] + result
	return result

if __name__ == '__main__':
	import sys
	print hex2base64(sys.argv[1])
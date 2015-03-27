
def set_up_text(text):
	return "comment1=cooking%20MCs;userdata=" + \
		   text.replace('&', "\"&\"").replace('=', "\"=\"") + \
		   ";comment2=%20like%20a%20pound%20of%20bacon"

if __name__ == '__main__':
	print set_up_text('a'*32)
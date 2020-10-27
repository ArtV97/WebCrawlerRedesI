from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
	imgsUrl = []

	def __init__(self):
		super().__init__()

	def handle_starttag(self, tag, attrs):
		if tag == "img":
			for i in range(len(attrs)):
				if attrs[i][0] == "src": #attrs eh uma lista de listas
					self.imgsUrl.append(attrs[i][1])

if __name__ == '__main__':
	parser = MyHTMLParser()
	parser.feed('<html><head><title>Test</title></head>'
			'<body><img src="boy.jpg" width="500"><h1>Parse me!</h1><img src="img_girl.jpg"></body></html>')
	print(parser.imgsUrl)
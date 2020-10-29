from socket import *
from MyHtmlParser import *

class webCrawler():
	def __init__(self, serverName, serverPort):
		self.serverName = serverName
		self.serverPort = serverPort
		self.clientSocket = None
		self.imagesUrl = []

	def connect(self):
		# Criacao do socket TCP
		self.clientSocket = socket(AF_INET, SOCK_STREAM)
		# Conexao com o servidor
		self.clientSocket.connect((self.serverName,self.serverPort))

	def send(self, request):
		self.clientSocket.sendall(request)

	def receive(self):
		return self.clientSocket.recv(4096)

	def close(self):
		self.clientSocket.close()

	def processHeader(self, stringResponse): #TO DO: melhorar processHeader
		pos = stringResponse.find(b"<!DOCTYPE html>")#retorna a posicao onde acaba o header
		header = stringResponse[:pos]
		cod = int(header[9:12]) #codigo retornado pelo servidor
		return cod, stringResponse[pos:]

	def receiveHtml(self):
		parser = MyHTMLParser()
		request = "GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(self.serverName)
		request = bytes(request, 'utf-8')
		self.connect()
		self.send(request)
		response = self.receive()
		cod, response = self.processHeader(response)
		if cod == 200:
			html = "" #variavel que armazenará o html
			arq = open("htmlBase.html", "w")
			while len(response) > 0: #enquanto houver dados no response
				parser.feed(str(response))
				html += response.decode("utf-8")
				for i in range (len(parser.imgsUrl)):
					src = parser.imgsUrl.pop()
					if src not in self.imagesUrl: self.imagesUrl.append(src)
				response = self.receive()
			arq.write(html)
			arq.close()
		else:
			print("Erro: A requisição retornou código: {}".format(cod))
		self.close()

	def receiveImgs(self): #TO DO: Parser do Header para checar cod do response
		for i in range(len(self.imagesUrl)):
			self.connect()
			imgExtension = self.imagesUrl[i][self.imagesUrl[i].find(".")+1:]
			request = "GET /{} HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(self.imagesUrl[i], self.serverName)
			request = bytes(request, 'utf-8')
			img = bytearray(b"")
			arq_img = open("imagem{}.{}".format(i+1, imgExtension), "wb")
			self.send(request)
			response = self.receive()
			response = response[response.rfind(b"\r\n\r\n")+4:]
			while len(response) > 0:
				img += response
				response = self.receive()
			arq_img.write(img)
			arq_img.close()
			self.close()

if __name__ == '__main__':
	import sys, getopt
	serverName = None
	serverPort = None
	try:
		opts, args = getopt.getopt(sys.argv[1:],"h:p:",["host=","port="])
	except getopt.GetoptError as err:
		print(err)
		print('HINT: webcrawler.py -h <host> -p <port>')
		sys.exit(1)
	for opt, arg in opts:
		if opt in ("-h", "--host"):
			serverName = arg
		elif opt in ("-p", "--port"):
			serverPort = int(arg)
	if(serverName == None or serverPort == None):
		print("Error: Missing Arguments")
		print('HINT: webcrawler.py -h <host> -p <port>')
		sys.exit(1)

	webcrawler = webCrawler(serverName, serverPort)
	webcrawler.receiveHtml()
	webcrawler.receiveImgs()
	print("Completed")

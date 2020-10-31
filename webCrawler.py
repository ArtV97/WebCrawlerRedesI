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

	#retorna header como dicionário e o body
	def parseResponse(self, response):
		pos = response.rfind(b"\r\n\r\n")
		splited_response = response[:pos].decode("utf-8").split("\r\n")
		first_line = splited_response[0].split(" ")
		header = {
					"http_version": first_line[0],
					"cod": int(first_line[1]),
					"cod_status": " ".join(first_line[2:])}
		for i in range(1, len(splited_response)):
			line = splited_response[i].split(": ")
			header[line[0]] = line[1]
		return header, response[pos+4:] #header, body

	def receiveHtml(self):
		parser = MyHTMLParser()
		request = "GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n".format(self.serverName)
		request = bytes(request, 'utf-8')
		self.connect()
		self.send(request)
		response = self.receive()
		header, body = self.parseResponse(response)
		if header["cod"] == 200:
			arq = open("htmlBase.html", "w")
			while len(body) < int(header["Content-Length"]): #enquanto houver dados no body
				parser.feed(str(body))
				for i in range (len(parser.imgsUrl)):
					src = parser.imgsUrl.pop()
					if src not in self.imagesUrl: self.imagesUrl.append(src)
				body += self.receive()
			arq.write(body.decode("utf-8"))
			arq.close()
		else:
			print("Erro: A requisição retornou código: {} {}".format(header["cod"], header["cod_status"]))
		self.close()

	def receiveImgs(self): #TO DO: Parser do Header para checar cod do response
		print(self.imagesUrl)
		self.connect()
		for i in range(len(self.imagesUrl)):
			request = "GET /{} HTTP/1.1\r\nHost: {}\r\n\r\n".format(self.imagesUrl[i], self.serverName)
			request = bytes(request, 'utf-8')
			self.send(request)
			response = self.receive()
			header, body = self.parseResponse(response)
			response = response[response.rfind(b"\r\n\r\n")+4:]
			if header["cod"] == 200:
				imgExtension = self.imagesUrl[i][self.imagesUrl[i].find(".")+1:]
				arq_img = open("imagem{}.{}".format(i+1, imgExtension), "wb")
				while len(body) < int(header["Content-Length"]):
					body += self.receive()
				arq_img.write(body)
				arq_img.close()
			else:
				print("Erro: A requisição da img retornou código: {} {}".format(header["cod"], header["cod_status"]))
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

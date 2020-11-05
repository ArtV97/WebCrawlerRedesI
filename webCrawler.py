from socket import *
from MyHtmlParser import *
import os

class webCrawler():
	def __init__(self, address, serverPort):
		self.address = address
		self.serverPort = serverPort
		self.serverName = None
		self.path = None
		self.clientSocket = None
		self.imagesUrl = []

	def parseAddress(self, address=None):
		address = address or self.address
		# Parsing do Endereço
		if "http://" in address:
			address = address.replace("http://", "")
		pos = address.find("/")
		if pos != -1:
			self.serverName = address[:pos]
			self.path = address[pos:]
		else: #index page
			self.serverName = address
			self.path = "/"
		print("Host:", self.serverName)
		print("Path:", self.path)

	def connect(self):
		# Criacao do socket TCP
		self.clientSocket = socket(AF_INET, SOCK_STREAM)
		# Conexao com o servidor
		self.clientSocket.connect((self.serverName,self.serverPort))

	def send(self, path=None):
		path = path or self.path
		if path[0] != "/": path = "/"+path
		request = "GET {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(path, self.serverName)
		request = bytes(request, 'utf-8')
		self.clientSocket.sendall(request)

	def receive(self):
		return self.clientSocket.recv(4096)

	def close(self):
		self.clientSocket.close()

	#retorna header como dicionário e o body
	def parseResponse(self, response):
		pos = response.find(b"\r\n\r\n")
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

	def checkTransfer(self, header, response, body):
		if "Content-Length" in header:
			return len(body) < int(header["Content-Length"])
		elif "Transfer-Encoding" in header:
			return b'0\r\n\r\n' not in response
		else:
			print("ERRO: O Servidor não forneceu informações sobre o conteúdo!")
			return False

	def receiveHtml(self):
		parser = MyHTMLParser()
		self.parseAddress()
		self.connect()
		self.send()
		response = self.receive()
		header, body = self.parseResponse(response)
		if header["cod"] == 200:
			arq = open("htmlBase.html", "w", encoding="utf-8")
			while self.checkTransfer(header, response, body):
				parser.feed(str(body))
				for src in parser.imgsUrl:
					if src not in self.imagesUrl: self.imagesUrl.append(src)
				parser.imgsUrl.clear() #esvazia lista
				response = self.receive()
				body += response
			arq.write(body.decode("utf-8"))
			arq.close()
		else:
			print("Erro: A requisição retornou código: {} {}".format(header["cod"], header["cod_status"]))
		self.close()

	def receiveImgs(self):
		self.connect()
		localPath = os.getcwd() + "/imagens"
		try:
			os.mkdir(localPath)
		except OSError: #diretório já existe
			for root, dirs, files in os.walk(localPath): #removendo imagens antigas do diretório
				for img in files: os.remove(os.path.join(root, img))
		for i in range(len(self.imagesUrl)):
			self.send(self.imagesUrl[i])
			response = self.receive()
			header, body = self.parseResponse(response)
			if header["cod"] == 200:
				pos = self.imagesUrl[i].rfind(".")
				imgName = self.imagesUrl[i][self.imagesUrl[i].rfind("/"):pos]
				imgName = localPath + imgName
				pos = header["Content-Type"].rfind("/")
				imgExtension = header["Content-Type"][pos+1:]
				print("Imagem salva em:", imgName + "."+ imgExtension)
				arq_img = open("{}.{}".format(imgName, imgExtension), "wb")
				while len(body) < int(header["Content-Length"]):
					body += self.receive()
				arq_img.write(body)
				arq_img.close()
			else:
				print("Erro: A requisição da img retornou código: {} {}".format(header["cod"], header["cod_status"]))
		self.close()

if __name__ == '__main__':
	import sys, getopt
	address = None
	serverPort = 80
	try:
		opts, args = getopt.getopt(sys.argv[1:],"a:p:",["address=","port="])
	except getopt.GetoptError as err:
		print(err)
		print('HINT: webcrawler.py -a <address> -p <port>')
		sys.exit(1)
	for opt, arg in opts:
		if opt in ("-a", "--address"):
			address = arg
		elif opt in ("-p", "--port"):
			serverPort = int(arg)
	if(address == None):
		print("Error: Missing Argument")
		print('HINT: webcrawler.py -a <address> -p <port>')
		sys.exit(1)

	webcrawler = webCrawler(address, serverPort)
	webcrawler.receiveHtml()
	webcrawler.receiveImgs()
	print("Completed")

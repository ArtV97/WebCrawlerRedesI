from socket import *
from MyHtmlParser import *

def processHeader(stringResponse):
	pos = stringResponse.find("<!DOCTYPE html>")#retorna a posicao onde acaba o header
	header = stringResponse[:pos]
	cod = int(header[11:14]) #codigo retornado pelo servidor
	return cod, stringResponse[pos:]


#serverName = 'www.tjsp.jus.br'
serverName = 'localhost'
#serverPort = 80
serverPort = 5500

# Criacao do socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# Conexao com o servidor
clientSocket.connect((serverName,serverPort))

#request = b"GET / HTTP/1.1\r\nHost: www.tjsp.jus.br\r\nConnection: close\r\n\r\n"
request = b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
# Envio de bytes
clientSocket.sendall(request)

# Recepcao
arq = open("htmlBase.html", "w")
parser = MyHTMLParser()
response = clientSocket.recv(4096)
cod, response = processHeader(str(response))
imagesUrl = []
if cod == 200:
	while response != b"": #enquanto houver dados no response
		parser.feed(str(response))
		arq.write(str(response))
		for i in range (len(parser.imgsUrl)):
				imagesUrl.append(parser.imgsUrl.pop())
		response = clientSocket.recv(4096)
	'''
	TO DO: Tratar imagens
	'''
else:
	print("Erro: A requisição retornou código: {}".format(cod))


print(imagesUrl)
# Fechamento
clientSocket.close()
arq.close()

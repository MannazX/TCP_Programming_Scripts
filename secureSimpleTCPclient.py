# computer networks TCPClient, page 191
from socket import *
import ssl

serverport = 12538
servername = "localhost"

clientSocket = socket(AF_INET, SOCK_STREAM)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
secureSocket = context.wrap_socket(clientSocket)
secureSocket.connect((servername, serverport))

while True:

    request = input("Input sentence: ")
    secureSocket.send(request.encode())
    response = secureSocket.recv(1024).decode()
    print("From server: ", response)
    if response.lower() == "exit":
        print("Exiting client")
        break

secureSocket.close()

